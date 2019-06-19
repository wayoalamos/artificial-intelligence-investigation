import numpy as np

def get_decision(prediction):
    max, ind = prediction[0], 0
    for i in range(1,4):
        if prediction[i] > max:
            max, ind = prediction[i], i
    ans = [0, 0, 0, 0]
    ans[ind] = 1
    return ans


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
        print("no move")
        return False, pos

    print("move down")
    temp = state[x][y]
    state[x][y] = state[x+1][y]
    state[x+1][y] = temp
    return state, (x+1, y)

def move_up(state, pos):
    x, y = pos
    if x == 0:
        print("no move")
        return False, pos

    print("move up")
    temp = state[x][y]
    state[x][y] = state[x-1][y]
    state[x-1][y] = temp
    return state, (x-1, y)

def move_right(state, pos):
    x, y = pos
    if y == 3:
        print("no move")
        return False, pos

    print("move right")
    temp = state[x][y]
    state[x][y] = state[x][y+1]
    state[x][y+1] = temp
    return state, (x, y+1)

def move_left(state, pos):
    x, y = pos
    if y == 0:
        print("no move")
        return False, pos

    print("move left")
    temp = state[x][y]
    state[x][y] = state[x][y-1]
    state[x][y-1] = temp
    return state, (x, y-1)

def test(model=""):
    print("TEST")
    last = "1000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001000000000000000010000000000000000100000000000000001"
    state  = "1000000000000000 0100000000000000 0000000001000000 0000000100000000 0000000000010000 0000000000000100 0000010000000000 0001000000000000 0000000000000010 0000000000001000 0000100000000000 0010000000000000 0000000010000000 0000001000000000 0000000000100000 0000000000000001"
    state = state.replace(" ", "")
    last = get_matrix(last)
    state = get_matrix(state)
    counter = 0

    while different(state,last) and counter < 40:
        counter += 1
        pos = find_pos(state)
        print("TEST: ", counter, pos)
        print_matrix(state)
        # move down
        # state, pos = move_right(state, pos)

        x_pred = get_x_array(state)
        y_pred = model.predict(x_pred)
        y = get_decision(y_pred[0])
        if y[0]:
            state, pos = move_left(state, pos)
        if y[1]:
            state, pos = move_down(state, pos)
        if y[2]:
            state, pos = move_right(state, pos)
        if y[3]:
            state, pos = move_up(state, pos)




#test()
