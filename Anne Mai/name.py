with open('names.txt', 'r') as file:
    next(file)  # Spring over headerlinjen
    for line in file:
        columns = line.split()
        approved_symbol = columns[1]
        print(approved_symbol)