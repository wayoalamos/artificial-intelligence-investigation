import numpy as np

def load_data():
    x_train = None
    y_train = None
    file_path = "../moves/problem_"
    file_end = "_.txt"
    for i in range(69):
        f = open(file_path+str(i)+file_end, "r")
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            line = line.split(",")
            x_sample = line[0].split()
            y_sample = line[1].split()

            if x_train is None:
                x_train, y_train = np.array([x_sample]), np.array([y_sample])
            else:
                x_train = np.append(x_train, [x_sample], axis=0)
                y_train = np.append(y_train, [y_sample], axis=0)
        f.close()
    return x_train, y_train

def load_evaluation_data():
    x_train = None
    y_train = None
    file_path = "../moves/problem_"
    file_end = "_.txt"
    for i in range(69,70):
        f = open(file_path+str(i)+file_end, "r")
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            line = line.split(",")
            x_sample = line[0].split()
            y_sample = line[1].split()

            if x_train is None:
                x_train, y_train = np.array([x_sample]), np.array([y_sample])
            else:
                x_train = np.append(x_train, [x_sample], axis=0)
                y_train = np.append(y_train, [y_sample], axis=0)
        f.close()
    return x_train, y_train
