import sys
from datetime import datetime
import hash
import data


def parse_csv(filename):
    index = 0
    data = []
    with open(filename, "r") as file:
        for line in file:
            if index == 0:
                index += 1
                continue
            line_filtered = [x.strip() for x in line.split(",")]
            data.append([line_filtered[0],
                         float(line_filtered[1]),
                         float(line_filtered[2]),
                         float(line_filtered[3]),
                         float(line_filtered[4]),
                         float(line_filtered[5]),
                         float(line_filtered[6])])
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
            print(f"Company: {name}")
            print(f"WKN: {wkn}")
            print(f"ID: {stock_id}")
            print(f"Date: {date}")
            print()
            print(f"Open: {open}$")
            print(f"High: {high}$")
            print(f"Low: {low}$")
            print(f"Close: {close}$")
            print(f"Adj Close: {adj_close}$")
            print(f"Volume: {volume}$")
        else:
            print("Stock not found")
            
    else:
        print("Stock not found")
    pass
def PLOT(stock_registry, stock):
    if not filter_arity(1, stock):
        return
    # Example data
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    data = [{"date": "2024-01-01", "price": 100},
            {"date": "2024-01-02", "price": 101},
            {"date": "2024-01-03", "price": 102}, 
            {"date": "2024-01-04", "price": 103}, 
            {"date": "2024-01-05", "price": 104}, 
            {"date": "2024-01-06", "price": 105}, 
            {"date": "2024-01-07", "price": 106}, 
            {"date": "2024-01-08", "price": 107}, 
            {"date": "2024-01-09", "price": 108}, 
            {"date": "2024-01-10", "price": 109}, 
            {"date": "2024-01-11", "price": 110}, 
            {"date": "2024-01-12", "price": 111}, 
            {"date": "2024-01-13", "price": 112},
            {"date": "2024-01-14", "price": 113}, 
            {"date": "2024-01-15", "price": 114}, 
            {"date": "2024-01-16", "price": 115}, 
            {"date": "2024-01-17", "price": 116},
            {"date": "2024-01-18", "price": 117},
            {"date": "2024-01-19", "price": 118},
            {"date": "2024-01-20", "price": 119},
            {"date": "2024-01-21", "price": 120},
            {"date": "2024-01-22", "price": 121},
            {"date": "2024-01-23", "price": 122},
            {"date": "2024-01-24", "price": 130},
            {"date": "2024-01-25", "price": 124},
            {"date": "2024-01-26", "price": 125},
            {"date": "2024-01-27", "price": 126},
            {"date": "2024-01-28", "price": 127},
            {"date": "2024-01-29", "price": 128},
            {"date": "2024-01-30", "price": 129},
            {"date": "2024-01-31", "price": 130}]
    
    # Sorts the data by price in descending order
    sorted_data = sorted(data, key=lambda x: x["price"], reverse=True)
    
    # Gets the price of the stock at the end date (today)
    today = list(filter(lambda x: x['date'] == end_date, sorted_data))

    # Helpers
    date_format = "%Y-%m-%d"
    horizontal_line = "+"+"-"*62+"+"
    to_date = lambda x: datetime.strptime(x, date_format)

    # Prints header
    print()
    print(f"Stock:      ${stock}")
    print(f"Price:      {today[0]['price']}$")
    print(f"Start date: {start_date}")
    print(f"End date:   {end_date}")
    print()

    # Prints the graph
    print(horizontal_line)
    for day in sorted_data:
        diff_end = to_date(end_date) - to_date(day['date'])
        diff_start = to_date(day['date']) - to_date(start_date)
        padding_left = " " * (diff_start.days * 2)
        padding_right = " " * (diff_end.days * 2)
        print("|"+padding_left+"$$"+padding_right+"| "+str(day['price'])+"$")
    print(horizontal_line)
    
def SAVE(stock_registry, args):
    if not filter_arity(1, args):
        return
    filename = args[0]
    table = stock_registry.table
    lookup = stock_registry.stock_lookup
    try:
        with open(filename, "w") as file:
            data = f"{table}"
            data = data.replace(" None", "")
            data = data.replace("[None", "[")
            file.write(data)
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
            table = data[0]
            lookup = data[1]
            table = table.replace("],,", "], None, ")
            table = table.replace(",,]", ", None, None]")
            table = table.replace(",, [", ", None, [")
            table = table.replace(",,", " None, None,")
            table = table.replace(",,", ", None,")
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
    result = function(stock_registry, *args)
    return result