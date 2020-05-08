import numpy as np
import sys

PUNISHMENT_FOR_VISIT = 1
MAX_COUNTER = 1000

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
            # y = get_decision(y_pred[0])
            s = ""
            for i in y_pred:
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
    print("No encontro la posicion del 0 upss..")
    sys.exit()
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
        # print("no move d",x ,y)
        return False

    # print("move down")
    temp = state[x][y]
    state[x][y] = state[x+1][y]
    state[x+1][y] = temp
    return state

def move_up(state, pos):
    x, y = pos
    if x == 0:
        # print("no move u",x ,y)
        return False

    # print("move up")
    temp = state[x][y]
    state[x][y] = state[x-1][y]
    state[x-1][y] = temp
    return state

def move_right(state, pos):
    x, y = pos
    if y == 3:
        # print("no move r",x ,y)
        return False

    # print("move right")
    temp = state[x][y]
    state[x][y] = state[x][y+1]
    state[x][y+1] = temp
    return state

def move_left(state, pos):
    x, y = pos
    if y == 0:
        # print("no move l",x ,y)
        return False

    # print("move left")
    temp = state[x][y]
    state[x][y] = state[x][y-1]
    state[x][y-1] = temp
    return state

def get_decision(model, state, pos, states_visited, counter_of_visits):
    x_pred = get_x_array(state)
    y_pred = model.predict(x_pred)
    y_pred = y_pred[0]

    ans = [(y_pred[i], i) for i in range(4)] # [(probabilidad, movimiento), (...), ... ]    

    # cambiar las probabilidades segun los estados visitados

    # fin de cambiar las probabilidades segun los visitados

    # cambiamos la opcion si es que no es posible y la ajustamos segun sus visitas
    index = 0
    already_punished = set()

    while index < 4:
        ans.sort(reverse=True)
        
        best_option = ans[index][1]
        state_copy = [[x for x in st] for st in state]
        if best_option == 0:
            possible_state = move_left(state_copy, pos)
        elif best_option == 1:
            possible_state = move_down(state_copy, pos)
        elif best_option == 2:
            possible_state = move_right(state_copy, pos)
        elif best_option == 3:
            possible_state = move_up(state_copy, pos)
        else:
            print("weird best option, siempre debiese ser un movimiento permitido entre 0 y 3")
            sys.exit()
        # revisamos si ya hemos visitado este nodo
                    
        if possible_state:

            if (not best_option in already_punished) and (possible_state in states_visited):
                index_visited = states_visited.index(possible_state) # TODO: no repetir esta busqueda!
                count = counter_of_visits[index_visited]
                # print("estado ya visitado! ups", index_visited, count)
                # print(ans)
                # cambiamos las probabilidades
                x, y = ans[index]
                x -= PUNISHMENT_FOR_VISIT * count
                ans[index] = (x, y)
                # fin cambiar las probabilidades
                already_punished.add(best_option)
                index = 0
                continue
                

            break
        index += 1
    if not possible_state:
        print("no se encontro ninguna opcion de movimiento posible, muy raro esto")
        sys.exit()
    # fin de cambiar la opcion si no es posible


    # change state for new_state
    for i in range(len(possible_state)):
        for j in range(len(possible_state[i])):
            state[i][j] = possible_state[i][j]
    # end changing actual state

    return state

def read_states():
    states = []
    fo = open('../15puzzle/problems')
    for s in fo.readlines():
        s = s.strip()
        s = s.split(" ")[1:]
        s = [int(x) for x in s]
        s = ["0"*i + "1" + "0"*(15-i) for i in s]
        s = " ".join(s)
        states.append(s)

    fo.close()

    return states


import random
def test(model=""):
    print("TEST")
    last = "1000000000000000 0100000000000000 0010000000000000 0001000000000000 0000100000000000 0000010000000000 0000001000000000 0000000100000000 0000000010000000 0000000001000000 0000000000100000 0000000000010000 0000000000001000 0000000000000100 0000000000000010 0000000000000001"

    states = read_states()

    last = last.replace(" ", "")
    last = get_matrix(last)

    state_number = 1
    for state in states:
        print("\n NUEVA ITERACION " + str(state_number))
        state_number += 1
        state = state.replace(" ", "")

        state = get_matrix(state)

        counter = 0

        states_visited = [] # almacena matrices de estados visitados
        counter_of_visits = {} # { index of the state in the list  states_visited: counter of visits to that state, ... }

        while different(state,last):
            counter += 1
            if counter > MAX_COUNTER:
                print("mayor a", MAX_COUNTER, ", no sigue")
                break

            pos = find_pos(state)
            
            # print(" ")
            # print("TEST: ", counter)
            # print_matrix(state)
            state = get_decision(model, state, pos, states_visited, counter_of_visits)

            if state is False:
                print("se callo el juego, movida prohibida, esto no deberia pasar")
                sys.exit()

            state_copy = [[x for x in st] for st in state]
            if state_copy in states_visited:
                index = states_visited.index(state_copy)
                counter_of_visits[index] += 1
            
            else:
                states_visited.append(state_copy)
                counter_of_visits[len(states_visited) - 1] = 1

        if not different(state, last):
            print("Se ha resuelto el problema en steps: ", counter)



#test()
