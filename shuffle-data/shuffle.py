import random

def read_lines_from_file():
    file = open("solutions_e.txt", "r")
    data = file.readlines()
    file.close()

    random.shuffle(data)

    file = open("solutions_e.txt", "w+")
    for line in data:
        file.write(line)
    file.close()

read_lines_from_file()
