
def parse_csv(filename):
    index = 0
    data = []
    with open(filename, "r") as file:
        for line in file:
            if index == 0:
                index += 1
                continue
            line = line.split(",")
            data.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6]])
