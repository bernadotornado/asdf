# implementation of a hash table with quadtratic probing
class StockRegistry:
    def __init__(self):
        # allocate memory
        self.capacity = 1009 # prime number
        self.table = [None] * self.capacity
        self.taken = 0

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
        # return none if not found on first pass
        if self.table[index] is None:
            return None
        else:
            collision = 1
            # checks h(k)+1, h(k)-1, h(k)+4, h(k)-4, h(k)+9, h(k)-9, ...
            # then test if stock id is the same, if not repeat
            while self.table[index] is not None:
                if self.table[index][0] == stock_id:
                    return self.table[index][1]
                if (index + 2 ** collision) % self.capacity is None:
                    index = (index + 2 ** collision) % self.capacity
                    break
                if (index - 2 ** collision) % self.capacity is None:
                    index = (index - 2 ** collision) % self.capacity
                    break
                collision += 1
            # return none if not found
            return None
        
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
