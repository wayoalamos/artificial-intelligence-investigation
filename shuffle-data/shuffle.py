import random

def read_lines_from_file():
    data = []
    for i in range(643):
        file_path = "../moves/bin-moves/1.1/sol_ida_problem_"+str(i)+"_.txt"
        file = open(file_path, "r")
        data += file.readlines();
    #print(data)
    print("length of data: ", len(data))
    file.close()

    random.shuffle(data)

    file = open("solutions.txt", "w+")
    for line in data:
        file.write(line)
    file.close()

read_lines_from_file()
