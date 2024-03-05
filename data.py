global data
data = []

def parse_csv(filename):
    with open(filename, "r") as file:
        for line in file:
            date, price = line.split(",")
            data.append(