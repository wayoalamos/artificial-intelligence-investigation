import numpy as np
import threading

lock = threading.Lock()

def load_data(batch_size, file, file_number, file_evaluation_number):
    lock.acquire()
    x_train, y_train = None, None
    for _ in range(batch_size):
        line = file.readline()
        if not line:
            file_number += 1
            file.close()
            if file_number >= file_evaluation_number:
                file_number = 0
            file_path = "../moves/bin-moves/1.1/sol_ida_problem_"
            file_end = "_.txt"
            file = open(file_path+str(file_number)+file_end, "r")
            line = file.readline()

        #print("aca:", file_number)
        #print(line)
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
    #print(LAST_FILE)
    #print("************evaluation: "+str(file_number))
    lock.release()
    return x_train, y_train, file, file_number

def load_data_e(batch_size, file, file_number, file_evaluation_number, file_last_number):
    lock.acquire()
    x_train, y_train = None, None
    for _ in range(batch_size):
        line = file.readline()
        if not line:
            file_number += 1
            file.close()
            if file_number >= file_last_number:
                file_number = file_evaluation_number
            file_path = "../moves/bin-moves/1.1/sol_ida_problem_"
            file_end = "_.txt"
            file = open(file_path+str(file_number)+file_end, "r")
            line = file.readline()

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
    #print(LAST_FILE)
    #print("************evaluation: "+str(file_number))
    lock.release()
    return x_train, y_train, file, file_number
