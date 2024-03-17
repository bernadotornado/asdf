# implementation of a hash table with quadtratic probing
class StockRegistry:


    # add a stock to the lookup table
    def add_stock(self, stock_id, wkn, name):
        self.stock_lookup.append([stock_id, wkn, name])
    # find a stock in the lookup table by id, wkn or name
    def find_stock(self, identifier, value):
        for stock in self.stock_lookup:
            if value in stock:
                match identifier:
                    case "id":
                            return stock[0]
                    case "wkn":
                            return stock[1]
                    case "name":
                            return stock[2]
        return None
    def __init__(self):
        # allocate memory
        self.capacity = 1009 # prime number
        self.table = [None] * self.capacity
        self.taken = 0
        self.stock_lookup = []
    
    def insert(self, stock_id, data):
        # check if the table is full
        if self.taken >= self.capacity:
            return 

        # calculate the index
        index = self.calculate_ascii_sum(stock_id) % self.capacity

        # attempt to insert the value without collision
        if self.table[index] is None:
            self.table[index] = [stock_id, data]
            self.taken += 1

        # collision
        else:
            collision = 1
            # checks h(k)+1, h(k)-1, h(k)+4, h(k)-4, h(k)+9, h(k)-9, ...
            while self.table[index] is not None:
                if (index + 2 ** collision) % self.capacity is None:
                    index = (index + 2 ** collision) % self.capacity
                    break
                if (index - 2 ** collision) % self.capacity is None:
                    index = (index - 2 ** collision) % self.capacity
                    break
                collision += 1
            self.table[index] = [stock_id, data]
            self.taken += 1

    def search(self, stock_id):
        index = self.calculate_ascii_sum(stock_id) % self.capacity
        # guard clause to prevent nonetype destructuring
        if self.table[index] is None:
            return None
        # return value if key is found on first pass
        if self.table[index][0] == stock_id:
            return self.table[index][1]
        else:
            collision = 1
            # checks h(k)+1, h(k)-1, h(k)+4, h(k)-4, h(k)+9, h(k)-9, ...
            # then test if stock id is the same, if not repeat
            while self.table[index][0] != stock_id:
                positive_offset = (index + 2 ** collision) % self.capacity
                negative_offset = (index - 2 ** collision) % self.capacity
                if collision > self.capacity:
                    break
                if self.table[positive_offset][0]==stock_id:
                    index = positive_offset
                    return self.table[index][1]
                if self.table[negative_offset][0]==stock_id:
                    index = negative_offset
                    return self.table[index][1]
              
                collision += 1
            # return none if not found
            return None
    def delete (self, stock_id):
        index = self.calculate_ascii_sum(stock_id) % self.capacity
        # guard clause to prevent freeing freed memory (False = key not found)
        if(self.table[index] is None):
            return False
        else:
            # delte if found on fist pass (True = found & freed)
            if(self.table[index][0] == stock_id):
                self.table[index] = None
                return True
            collision = 1
            while(self.table[index][0] != stock_id):
                # TODO: implement delete
                if(index + 2** collision) % self.capacity :
                    break
    

    # converts the stock id to an integer with weights 10^i for each character
    def calculate_ascii_sum(self, stock_id):
        ascii_sum = 0
        weights = [10 ** i for i in range(len(stock_id))]

        for i, letter in enumerate(stock_id):
            ascii_sum += ord(letter) * weights[i]

        return ascii_sum

# test 
if __name__ == '__main__':
    stocks = StockRegistry()
    stocks.insert("AAPL", 129)
    stocks.insert("MSFT", 130)
    stocks.insert("TSLA", 131)
    stocks.insert("GOOG", 132)
    stocks.insert("AMZN", 133)
    stocks.insert("META", 134)
    stocks.insert("NVDA", 135)
    stocks.insert("INTC", 136)
    stocks.insert("CSCO", 137)
    stocks.insert("ADBE", 138)
    stocks.insert("PYPL", 139)
    stocks.insert("NFLX", 140)
    stocks.insert("CMCSA", 141)

    print(stocks.table)
    print(stocks.search("MSFT"))
    print(stocks.search("AAPL"))
    print(stocks.search("GOOG"))
    print(stocks.search("CMCSA"))
    print(stocks.search("TEST"))

    print(stocks.delete("TEST"))
    stocks.delete("AAPL")
    
    print(stocks.search("AAPL"))
    stocks.add_stock("AAPL", "0123123", "Apple")
    print(stocks.find_stock("id", "Apple"))
