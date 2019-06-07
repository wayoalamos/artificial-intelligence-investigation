import numpy as np

# nn has 16x16 input neurons and output 4

def load_data():
    x_train = None
    y_train = None
    file_path = "../moves-example-one-bin/bin_problem_"
    file_end = "_.txt"
    for i in range(65):
        f = open(file_path+str(i)+file_end, "r")
        while True:
            line = f.readline()
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
        f.close()
    return x_train, y_train

def load_evaluation_data():
    x_train = None
    y_train = None
    file_path = "../moves-example-one-bin/bin_problem_"
    file_end = "_.txt"
    for i in range(65,70):
        f = open(file_path+str(i)+file_end, "r")
        while True:
            line = f.readline()
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
        f.close()
    return x_train, y_train
