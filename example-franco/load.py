import sys
import numpy as np
from numpy import genfromtxt
from model_info import get_model_info

import threading

X_data = None # UNUSED
Y_data = None # UNUSED

X_data_files = []
Y_data_file  = None 

number_of_features           = 0
total_number_of_samples      = 0
training_number_of_samples   = 0
validation_number_of_samples = 0

lock = threading.Lock()

def load_nn_data(model_file):
    global X_data_files, Y_data_file
    global number_of_features, total_number_of_samples

    # Files
    path_training_set_data = model_file
    path_training_set_in   = model_file + "_in_{}.txt"
    path_training_set_out  = model_file + "_out.txt"

    # Info
    model_info = get_model_info(model_file)
    number_of_features = model_info['n_inputs']
    
    # Open input files
    for i in range(number_of_features):
        path = path_training_set_in.format(model_info['input'][i]['name'])
        X_data_files.append(open(path))
    
    # Open output file    
    Y_data_file = open(path_training_set_out)

    # Count the number of samples (including # lines)
    total_number_of_samples = sum(1 for line in Y_data_file)
    Y_data_file.seek(0)
    print("total_number_of_samples:" + str(total_number_of_samples))
    
    return model_info

def nn_read_sample(cut=False):
    global X_data_files, Y_data_file
    lock.acquire()
    
    X_sample = []
    #print("reading y line")
    Y_sample = Y_data_file.readline()
    
    for f in X_data_files:
        line = f.readline()
        X_sample.append(line)

    if "#" in Y_sample:
        lock.release()
        if cut:
            return None, None
        else:
            return nn_read_sample()

    # if the EOF is reached
    if len(Y_sample.strip()) == 0:
        # start again
        Y_data_file.seek(0)
        for f in X_data_files:
            f.seek(0)
        lock.release()
        return nn_read_sample()

    # Parse every sample
    Y_sample_old = Y_sample
    Y_sample = np.fromstring(Y_sample, sep=' ')

    for i in range(len(X_sample)):
        X_sample[i] = np.fromstring(X_sample[i], sep=' ')

    lock.release()
    return X_sample, Y_sample

def nn_read_samples(n):
    X = [[] for _ in range(number_of_features)]
    Y = []

    # Collect n samples
    for i in range(n):
        X_sample, Y_sample = nn_read_sample()

        for k in range(number_of_features):
            X[k].append(X_sample[k])

        Y.append(Y_sample)

    # Parse to numpy array
    Y = np.array(Y)

    for k in range(number_of_features):
        X[k] = np.array(X[k])
    
    #return [X, Y]

    X2 = []
    for i in range(n):
        x = X[0][i]
        for k in range(number_of_features - 1):
            x = np.concatenate([x, X[k + 1][i]])
        X2.append(x)

    X2 = np.array(X2)

    return [X2, Y]

def nn_read_samples_until_cut():
    X = [[] for _ in range(number_of_features)]
    Y = []

    # Collect n samples
    n = 0
    while True:
        X_sample, Y_sample = nn_read_sample(True)

        if X_sample is None or Y_sample is None:
            break;

        for k in range(number_of_features):
            X[k].append(X_sample[k])

        Y.append(Y_sample)
        n = n + 1

    # Parse to numpy array
    Y = np.array(Y)

    for k in range(number_of_features):
        X[k] = np.array(X[k])
    
    #return [X, Y]

    X2 = []
    for i in range(n):
        x = X[0][i]
        for k in range(number_of_features - 1):
            x = np.concatenate([x, X[k + 1][i]])
        X2.append(x)

    X2 = np.array(X2)

    return [X2, Y]    


def nn_generator(batch_size):
    while 1:
        yield nn_read_samples(batch_size)

def nn_validation_generator():
    while 1:
        yield nn_read_samples(validation_number_of_samples)

def get_generator(batch_size, validation_split):
    global training_number_of_samples, validation_number_of_samples

    training_number_of_samples   = int((1 - validation_split) * total_number_of_samples)
    validation_number_of_samples = int(validation_split * total_number_of_samples)
    
    training_size   = training_number_of_samples
    validation_size = validation_number_of_samples

    return nn_generator(batch_size), nn_validation_generator(), training_size, validation_size




