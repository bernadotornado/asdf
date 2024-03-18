import sys
from datetime import datetime
import math
import hash
import data


def parse_csv(filename):
    index = 0
    data = []
    with open(filename, "r") as file:
        for line in file:
            # skip the first line
            if index == 0:
                index += 1
                continue
            line_filtered = [x.strip() for x in line.split(",")]
            data.append([line_filtered[0], # date
                         float(line_filtered[1]), # open
                         float(line_filtered[2]), # high
                         float(line_filtered[3]), # low
                         float(line_filtered[4]), # close
                         float(line_filtered[5]), # adj_close
                         float(line_filtered[6])])# volume
            index += 1

    return data 

# ERROR guard when the number of arguments is not correct
def filter_arity(arity, args):
    if len(args) != arity:
        ERROR(f"Expected {arity} arguments, got {len(args)}\n")
        return False
    return True
def ADD(stock_registry, stock):
    if not filter_arity(3, stock):
        return
    print(f"Added {stock[0]}, {stock[1]}, {stock[2]} to the stock registry.")
    stock_registry.add_stock(stock[0], stock[1], stock[2])
    pass
def DEL(stock_registry, stock):
    if not filter_arity(1, stock):
        return
    # get data from lookup table
    id = stock_registry.find_stock("id", stock[0])
    name = stock_registry.find_stock("name", stock[0])
    wkn = stock_registry.find_stock("wkn", stock[0])
    if id is not None:
        # delete stock from lookup table (true if successful, false if not)
        res = stock_registry.delete_stock(id)
        if res:
            print(f"Deleting {name}, {wkn} {id} from the stock registry.")
            # delete stock from hash table
            stock_registry.delete(id)
        else:
            print(f"Stock {stock[0]} not found")
    else:
        print(f"Stock {stock[0]} not found")
    pass
def IMPORT(stock_registry, args):
    if not filter_arity(2, args):
        return
    # parse csv file from args[0]
    data = parse_csv(args[0])
    # get data from lookup table
    id = stock_registry.find_stock("id", args[1])
    name = stock_registry.find_stock("name", args[1])
    wkn = stock_registry.find_stock("wkn", args[1])
    if id is not None:
        # insert data into hash table
        stock_registry.insert(id, data)
        print(f"Importing {args[0]} into {name}, {wkn} {id}")
    else:
        print(f"Stock {args[1]} not found")
        
def SEARCH(stock_registry, stock):
    if not filter_arity(1, stock):
        return
    print(f"Searching {stock}")
    stock_id = stock_registry.find_stock("id", stock[0])
    name = stock_registry.find_stock("name", stock[0])
    wkn = stock_registry.find_stock("wkn", stock[0])
    if stock_id is not None:
        stock = stock_registry.search(stock_id)
        if stock is not None:
            # get last entry data and destructure it
            [date, open, high, low, close, adj_close, volume] = stock[:1][0]
            # print data
            print(f"Company:   {name}")
            print(f"WKN:       {wkn}")
            print(f"ID:        {stock_id}")
            print(f"Date:      {date}")
            print()
            print(f"Open:      ${open}")
            print(f"High:      ${high}")
            print(f"Low:       ${low}")
            print(f"Close:     ${close}")
            print(f"Adj Close: ${adj_close}")
            print(f"Volume:    ${volume}")
        else:
            print("Stock not found")
            
    else:
        print("Stock not found")
    pass
def PLOT(stock_registry, stock):
    if not filter_arity(1, stock):
        return
    # get data from lookup table
    stock_id = stock_registry.find_stock("id", stock[0])
    # guard clause to prevent nonetype
    if stock_id is None:
        print(f"Stock {stock[0]} not found")
        return
    
    # Helpers
    date_format = "%Y-%m-%d"
    to_date = lambda x: datetime.strptime(x, date_format)
    name = stock_registry.find_stock("name", stock[0])
    wkn = stock_registry.find_stock("wkn", stock[0])
    data = stock_registry.search(stock_id)
    data = data[:30]
    start_date = data[0][0]
    end_date = data[-1][0]
    diff_days = (to_date(end_date) - to_date(start_date)).days
    horizontal_line = "+"+"-"*(diff_days+1)+"+"

    # Prints header
    print()
    print(f"Company:    {name}")
    print(f"WKN:        {wkn}")
    print(f"ID:         {stock_id}")
    print(f"Start date: {start_date}")
    print(f"End date:   {end_date}")
    print()

    sorted_data = {}
    # Groups data by price
    for line in data:
        date = to_date(line[0])
        diff_start = (date-to_date(start_date)).days
        price = math.floor(line[4])
        price = f"{price}"
        if price in sorted_data:
        # Key exists, append diff_start to the existing list
            sorted_data[price].append(diff_start)
        else:
        # Key does not exist, create a new list with diff_start
            sorted_data[price] = [diff_start]
    
    # Sorts the data by price in descending order
    sorted_data = dict(sorted(sorted_data.items(), key=lambda x: int(x[0]), reverse=True))

    # Prints the graph
    print(horizontal_line)
    for price in sorted_data:
        # blank string with length diff_days+1
        str = " "*(diff_days+1)
        for day in sorted_data[price]:
            # insert diff_days (x) of price (y) into blank string
            str = str[:day] + "$" + str[day+1:]
        # print the string with formatting and price
        print(f"|{str}| {price}$")
    print(horizontal_line)
    
def SAVE(stock_registry, args):
    if not filter_arity(1, args):
        return
    filename = args[0]
    table = stock_registry.table
    lookup = stock_registry.stock_lookup
    try:
        with open(filename, "w") as file:
            # dump hash table on the first line, replace None with empty string
            data = f"{table}"
            data = data.replace(" None", "")
            data = data.replace("[None", "[")
            file.write(data)
            # dump lookup table on the next line
            file.write("\n")
            file.write(f"{lookup}")
        print(f"Saving to {filename}")
    except:
        print(f"Could not save to {filename}")
    
def LOAD(stock_registry, args):

    if not filter_arity(1, args):
        return
    filename = args[0]
    try:
        with open(filename, "r") as file:
            data = file.readlines()
            print(f"Loading from {filename}")
            # load hash table from the first line
            table = data[0]
            # load lookup table from the next line
            lookup = data[1]
            # replace empty string with None (and edge cases)
            table = table.replace("],,", "], None, ")
            table = table.replace(",,]", ", None, None]")
            table = table.replace(",, [", ", None, [")
            table = table.replace(",,", " None, None,")
            table = table.replace(",,", ", None,")
            # evaluate the strings to get the actual data, save it to the stock_registry
            stock_registry.table =eval(table)
            stock_registry.stock_lookup = eval(lookup)
    except:
        print(f"Could not load from {filename}")
        
def QUIT():
    sys.exit(0)
def ERROR(msg):
    print("ERROR: "+msg)
    pass
def call(stock_registry, function_name, *args):
    # get correct function 
    match function_name:
        case "ADD":     function = ADD
        case "DEL":     function = DEL
        case "IMPORT":  function = IMPORT
        case "SEARCH":  function = SEARCH
        case "PLOT":    function = PLOT
        case "SAVE":    function = SAVE
        case "LOAD":    function = LOAD
        case "QUIT":    function = QUIT
        case _:
            ERROR("Invalid command")
            return 
    # call function with the registry and the arguments
    result = function(stock_registry, *args)
    return result