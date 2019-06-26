import numpy as np

def test_with_data(model):
    print("TEST")
    counter = 0
    total = 0
    for i in range(21):
        path = "../moves/bin-moves/sol_ida_problem_"+str(i)+"_.txt"
        file = open(path, 'r')
        for line in file.readlines():
            line = line.replace(" ", "")
            solution = line[-5:].strip() # last 4 chars
            line = line[:-5] # all line except the solution
            x_pred = np.array([list(line)]).astype('f')
            y_pred = model.predict(x_pred)
            y = get_decision(y_pred[0])
            s = ""
            for i in y:
                s += str(i)

            if(s == solution):
                counter += 1
            total += 1
        file.close()
    print(total)
    print(counter)
    print(float(counter)/float(total))

def find_pos(line):
    cero = "1000000000000000"
    for i in range (4):
        for j in range(4):
            if line[i][j] == cero:
                return (i, j)
    return None

def get_matrix(line):
    list_line = [[],[],[],[]]
    for i in range(4):
        for j in range(4):
            list_line[i].append(line[i*16*4 + j*16 : i*16*4 + j*16+16])
    return list_line

def print_matrix(matrix):
    for i in range(4):
        row = ""
        for j in range(4):
            x = matrix[i][j].find("1")
            row += str(x) + " "
            if x < 10:
                row += " "
        print(row)

def different(matrix1, matrix2):
    for i in range(4):
        for j in range(4):
            if matrix1[i][j] != matrix2[i][j]:
                return True
    return False

def get_x_array(matrix):
    line = ""
    for i in range(4):
        for j in range(4):
            line += matrix[i][j]
    return np.array([list(line)]).astype('f')

def move_down(state, pos):
    x, y = pos
    if x == 3:
        print("no move d",x ,y)
        return False, pos

    print("move down")
    temp = state[x][y]
    state[x][y] = state[x+1][y]
    state[x+1][y] = temp
    return state, (x+1, y)

def move_up(state, pos):
    x, y = pos
    if x == 0:
        print("no move u",x ,y)
        return False, pos

    print("move up")
    temp = state[x][y]
    state[x][y] = state[x-1][y]
    state[x-1][y] = temp
    return state, (x-1, y)

def move_right(state, pos):
    x, y = pos
    if y == 3:
        print("no move r",x ,y)
        return False, pos

    print("move right")
    temp = state[x][y]
    state[x][y] = state[x][y+1]
    state[x][y+1] = temp
    return state, (x, y+1)

def move_left(state, pos):
    x, y = pos
    if y == 0:
        print("no move l",x ,y)
        return False, pos

    print("move left")
    temp = state[x][y]
    state[x][y] = state[x][y-1]
    state[x][y-1] = temp
    return state, (x, y-1)

def get_decision(model, state, pos, states_visited):
    x_pred = get_x_array(state)
    y_pred = model.predict(x_pred)
    y_pred = y_pred[0]

    ans = [(y_pred[i], i) for i in range(4)]
    ans.sort()
    ans.reverse()
    ans = [i[1] for i in ans]
    for i in range(4):
        if ans[i] == 0:
            possible_state, possible_pos = move_left(state, pos)
        elif ans[i] == 1:
            possible_state, possible_pos = move_down(state, pos)
        elif ans[i] == 2:
            possible_state, possible_pos = move_right(state, pos)
        elif ans[i] == 3:
            possible_state, possible_pos = move_up(state, pos)
        if possible_state is False:
            print("not possible move")
            if i == 3:
                print("ya no hay mas posibles movidas :(")
                return False, False
            continue
        if possible_state in states_visited:
            print("already in visited")
            if i == 3:
                print("ya no hay mas posibles movidas :(")
                return False, False
            continue
        break
    return possible_state, possible_pos

import random
def test(model=""):
    print("TEST")
    last = "1000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001"
    state  = "1000000000000000 0100000000000000 0000000001000000 0000000100000000 0000000000010000 0000000000000100 0000010000000000 0001000000000000 0000000000000010 0000000000001000 0000100000000000 0010000000000000 0000000010000000 0000001000000000 0000000000100000 0000000000000001"

    state = state.replace(" ", "")
    last = last.replace(" ", "")

    state = get_matrix(state)
    last = get_matrix(last)

    counter = 0

    states_visited = []

    while different(state,last) and counter < 300:
        pos = find_pos(state)
        counter += 1
        print("TEST: ", counter)
        print_matrix(state)
        state, pos = get_decision(model, state, pos, states_visited)

        if state is False:
            print("se callo el juevo, movida prohibida, esto no deberia pasar")
            return

        state_copy = [[x for x in st] for st in state]
        states_visited.append(state_copy)


    if not different(state, last):
        print("Se ha resuelto el problema en steps: ", counter)



#test()
