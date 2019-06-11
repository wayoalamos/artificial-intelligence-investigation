import numpy as np
import threading

lock = threading.Lock()

def load_data(batch_size, file):
    lock.acquire()
    x_train, y_train = None, None
    print("acaAAAAAAAAAb")

    for _ in range(batch_size):
        print("acaAAAAAAAAA")
        line = file.readline()
        if not line:
            break
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
    return x_train, y_train, file

def load_data_e(batch_size, file):
    lock.acquire()
    x_train, y_train = None, None
    for _ in range(batch_size):
        line = file.readline()
        if not line:
            break
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
    return x_train, y_train, file
