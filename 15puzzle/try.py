#  ./ida < problems0

import os

# create 10 new problems in file problems0

# from file convert the file to bin moves
# repeat!

PROBLEMS_IN_FILE = 144

def transform_to_bin(path, new_path):
    file = open(path, "r+")
    new_file = open(new_path, "w+")
    line = [
    "1000000000000000",
    "0100000000000000",
    "0010000000000000",
    "0001000000000000",
    "0000100000000000",
    "0000010000000000",
    "0000001000000000",
    "0000000100000000",
    "0000000010000000",
    "0000000001000000",
    "0000000000100000",
    "0000000000010000",
    "0000000000001000",
    "0000000000000100",
    "0000000000000010",
    "0000000000000001"
    ]
    last_position = 0
    for num in file.readlines():
        num = int(num.strip())
        move = False
        if (num - last_position) == 1: # move to the left
            move = 1
        if (num - last_position) == -4: # move down
            move = 2
        if (num - last_position) == -1: # move to the right
            move = 3
        if (num - last_position) == 4: #move up
            move = 4
        temp = line[last_position]
        line[last_position] = line[num]
        line[num] = temp
        str_bin = ["0", "0", "0", "0"]
        str_bin[move-1] = "1"
        to_write = " ".join(line)+" "+ "".join(str_bin)
        last_position = num
        new_file.write(to_write + "\n")
    file.close()

import random
def create_new_problems(number, file):
    def print_matrix(matrix):
        for i in matrix:
            print (i)
    def create_new_matrix(matrix):
        for i in range(300):
            move = random.randint(0,3)
            if (i < 30):
                for _ in range(random.randint(1,3)):
                    index_0 = None
                    for i3 in range(4):
                        for j3 in range(4):
                            if matrix[i3][j3] == 0:
                                index_0 = (i3,j3)
                    if index_0 == None:
                        print("ERRORRRRRRRRRRRRRRRRRRRRRRRRRRR NO ENCONTRO EL 0")
                    # se hacen 10 movimientos randoms
                    x, y = index_0
                    if move == 0 and y == 0:
                        continue
                    if move == 1 and x == 3:
                        continue
                    if move == 2 and y == 3:
                        continue
                    if move == 3 and x == 0:
                        continue
                    # the movement is possible
                    if move == 0:
                        matrix[x][y] = matrix[x][y-1]
                        matrix[x][y-1] = 0
                    if move == 1:
                        matrix[x][y] = matrix[x+1][y]
                        matrix[x+1][y] = 0
                    if move == 2:
                        matrix[x][y] = matrix[x][y+1]
                        matrix[x][y+1] = 0
                    if move == 3:
                        matrix[x][y] = matrix[x-1][y]
                        matrix[x-1][y] = 0
            else:
                index_0 = None
                for i3 in range(4):
                    for j3 in range(4):
                        if matrix[i3][j3] == 0:
                            index_0 = (i3,j3)
                if index_0 == None:
                    print("ERRORRRRRRRRRRRRRRRRRRRRRRRRRRR NO ENCONTRO EL 0")
                # se hacen 10 movimientos randoms
                x, y = index_0
                if move == 0 and y == 0:
                    continue
                if move == 1 and x == 3:
                    continue
                if move == 2 and y == 3:
                    continue
                if move == 3 and x == 0:
                    continue
                # the movement is possible
                if move == 0:
                    matrix[x][y] = matrix[x][y-1]
                    matrix[x][y-1] = 0
                if move == 1:
                    matrix[x][y] = matrix[x+1][y]
                    matrix[x+1][y] = 0
                if move == 2:
                    matrix[x][y] = matrix[x][y+1]
                    matrix[x][y+1] = 0
                if move == 3:
                    matrix[x][y] = matrix[x-1][y]
                    matrix[x-1][y] = 0
        #print_matrix(matrix)
        return matrix

    def write_in_file(i, foo, matrix):
        i_w = str(i)
        if i < 10:
            i_w = '0' + str(i)
        foo.write(str(i_w))
        for i2 in range(4):
            for j in range(4):
                foo.write( ' ' + str(matrix[i2][j]))
        foo.write('\n')


    matrix = [[14, 1, 9, 6], [4, 8, 12, 5], [7, 2, 3, 0], [10, 11, 13, 15]]
    foo = open(file, 'w')
    for i in range(number):
        create_new_matrix(matrix)
        write_in_file(i+1, foo, matrix)
    foo.close()

counter = -1
#11070
#11794
#12802
#19714
#21442
#24177
#25616 
starting_point = 26335
while True:
    counter += 1
    print("starting while loop with counter", counter, "# file", starting_point + counter*PROBLEMS_IN_FILE)
    create_new_problems(145, 'problems0')
    os.system("./ida < problems0")
    path = "../moves-from-generated-data/ida_problem_0_.txt"
    new_path = "../moves/bin-moves/sol_ida_problem_0_.txt"
    for i in range(PROBLEMS_IN_FILE):
        path = path[:41] + str(i) + "_.txt"
        new_path = new_path[:35] + str(starting_point + counter*PROBLEMS_IN_FILE + i) + "_.txt"
        transform_to_bin(path, new_path)
