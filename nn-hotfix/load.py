import numpy as np
import threading
import random

# files:
# PROBLEMS = 22177
# VALIDATION = 2000
# TOTAL = 24177

lock = threading.Lock()

def load_files(data, initial, final):
    for i in range(initial, final):
        fo = open('../moves/bin-moves/sol_ida_problem_'+str(i)+'_.txt')
        for l in fo.readlines():
            data.append(l)
        fo.close()
    random.shuffle(data)
    return data

def load_data(batch_size, data):
    lock.acquire()
    x_train, y_train = None, None
    for _ in range(batch_size):
        if len(data) < 2:
            print('CARGAR DATOS OTRA VEZ!')
            data = load_files(data, 0, 23177)
        line = data.pop() # esto deberia ser random
        if len(data) % 100000 == 0:
            print("  ---->", len(data))
        solution = line[-5:] # last 4 chars
        line = line[:-5] # all line except the solution
        line = line.replace(" ", "")
        x_sample = np.array([list(line)]).astype('f')
        y_sample = np.array([list(solution.rstrip())]).astype('f')

        if x_train is None:
            x_train, y_train = x_sample, y_sample
        else:
            x_train = np.append(x_train, x_sample, axis=0)
            y_train = np.append(y_train, y_sample, axis=0)

    lock.release()
    return x_train, y_train

def load_data_e(batch_size, data):
    lock.acquire()
    x_train, y_train = None, None
    for _ in range(batch_size):
        line = random.choice(data)
        solution = line[-5:] # last 4 chars
        line = line[:-5] # all line except the solution
        line = line.replace(" ", "")
        x_sample = np.array([list(line)]).astype('f')
        y_sample = np.array([list(solution.rstrip())]).astype('f')

        if x_train is None:
            x_train, y_train = x_sample, y_sample
        else:
            x_train = np.append(x_train, x_sample, axis=0)
            y_train = np.append(y_train, y_sample, axis=0)


    #print("VALIDATING"+str(VAL))
    """print("x_train")
    print(x_train)
    print("y_train")
    print(y_train)
    """
    lock.release()
    return x_train, y_train
