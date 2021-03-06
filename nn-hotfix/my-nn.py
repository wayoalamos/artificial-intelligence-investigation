from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Concatenate # Merge
from keras.layers.merge import concatenate
from keras.optimizers import Adam
from load import load_data, load_data_e
from test import test

import sys
import random

# training
import os
os.environ["THEANO_FLAGS"] = "device=cpu,floatX=float32,mode=FAST_RUN,allow_gc=False"
from keras.utils.vis_utils import plot_model
import numpy as np

FILE_NAME = "model_diagram"

TRIANING_FILES = 23177
VALIDATION_FILES =  1000
#TOTAL_FILES = 24177

# STATES = 1133410
STATES = 1133410
VALIDATION = 52075
# TOTAL_STATES = 1185485


training_data = []
validation_data = []



# load
def create_nn(n_input_layers, n_output_layers):
    # Creates the NN model, then return it.

    # Input layer
    input = Input(shape = (n_input_layers,))

    # Hidden layer
    hidden_layer = Dense(units=16*10, activation='relu')(input)
    hidden_layer = Dense(units=16*5, activation='relu')(hidden_layer)
    hidden_layer = Dense(units=16, activation='relu')(hidden_layer)
    #hidden_layer = Dense(units=16, activation='relu')(hidden_layer)

    # Output layer
    output_layer = Dense(units=n_output_layers, activation='softmax')(hidden_layer)

    model = Model(inputs=input, outputs=output_layer)

    # Compile
    optimizer = Adam()
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model

# training
def nn_read_samples(batch_size):
    global training_data
    x_sample, y_sample = load_data(batch_size, training_data)
    return [x_sample, y_sample]

def nn_read_evaluation_samples(batch_size):
    global validation_data
    x_sample, y_sample = load_data_e(batch_size, validation_data)
    return [x_sample, y_sample]

def generator(batch_size):
    while 1:
        yield nn_read_samples(batch_size)

def validation_generator(batch_size):
    while 1:
        yield nn_read_evaluation_samples(batch_size)

def see_weights(model):
    for capa in model.layers:
        print("weights: ", capa.get_weights())

def load_files(data, initial, final):
    for i in range(initial, final):
        fo = open('../moves/bin-moves/sol_ida_problem_'+str(i)+'_.txt')
        for l in fo.readlines():
            data.append(l)
        fo.close()
    random.shuffle(data)
    


load_files(training_data, 0, TRIANING_FILES + 1)
load_files(validation_data, TRIANING_FILES + 1, TRIANING_FILES + 1001)

# print(len(training_data))
# print(len(validation_data))

# see_weights(model)
#PROBLEMS =  11000
#VALIDATION = 9667

BATCH_SIZE = 300
EPOCHS = 8

STEPS_PER_EPOCH = int(STATES/BATCH_SIZE) # cuantos batches tomo por epoch -> ideal : total/batchsize
VALIDATION_STEPS = int(VALIDATION/BATCH_SIZE)

TEST_MODE = False

if __name__ == "__main__":

    model = create_nn(16*16,4)
    # plot_model(model, to_file=(FILE_NAME + '.png'), show_shapes=True)
    # model.summary()

    model.fit_generator(
                    epochs=EPOCHS,
                    generator=generator(BATCH_SIZE),
                    steps_per_epoch=STEPS_PER_EPOCH, # cambiar
                    validation_data=validation_generator(BATCH_SIZE),
                    validation_steps=VALIDATION_STEPS,
                    verbose=1
                    )

    print("*evalution*")
    evaluation = model.evaluate_generator(
                   generator=validation_generator(BATCH_SIZE),
                   steps=BATCH_SIZE,
                   verbose=1
                   )
    print(evaluation)
    model.save('15puzzle_solver_model.h5')

    if TEST_MODE:
        test(model)

    import time
    time.sleep(1)
