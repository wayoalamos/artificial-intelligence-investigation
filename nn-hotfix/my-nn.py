from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Concatenate # Merge
from keras.layers.merge import concatenate
from keras.optimizers import Adam
from load import load_data, load_data_e

import sys

# training
import os
os.environ["THEANO_FLAGS"] = "device=cpu,floatX=float32,mode=FAST_RUN,allow_gc=False"
from keras.utils.vis_utils import plot_model
import numpy as np

FILE_NAME = "model_diagram"

FILE = open("../shuffle-data/solutions.txt", "r")
FILE_E = open("../shuffle-data/solutions_e.txt", "r")


# load
def load_nn(n_input_layers, n_output_layers):
    # Creates the NN model, then return it.

    # Input layer
    input = Input(shape = (n_input_layers,))

    # Hidden layer
    hidden_layer = Dense(units=16*5, activation='relu')(input)
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
    global FILE
    x_sample, y_sample, FILE = load_data(batch_size, FILE)
    return [x_sample, y_sample]

def nn_read_evaluation_samples(batch_size):
    global FILE_E
    x_sample, y_sample, FILE_E = load_data_e(batch_size, FILE_E)
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

# see_weights(model)
def get_decision(prediction):
    max, ind = prediction[0], 0
    for i in range(1,4):
        if prediction[i] > max:
            max, ind = prediction[i], i

    ans = [0, 0, 0, 0]
    ans[ind] = 1

    return ans

# generator(20)
# print(nn_read_evaluation_samples(20))


model = load_nn(16*16,4)
plot_model(model, to_file=(FILE_NAME + '.png'), show_shapes=True)
#model.summary()

PROBLEMS =  11000      # 20 60 20 100
VALIDATION = 9667

BATCH_SIZE = 50
STEPS_PER_EPOCH = int(PROBLEMS/BATCH_SIZE) # cuantos batches tomo por epoch -> ideal : total/batchsize
VALIDATION_STEPS = int(VALIDATION/BATCH_SIZE)


model.fit_generator(
                epochs=40,
                generator=generator(BATCH_SIZE),
                steps_per_epoch=STEPS_PER_EPOCH, # cambiar
                validation_data=validation_generator(BATCH_SIZE),
                validation_steps=VALIDATION_STEPS,
                # verbose=1
                )

print("*evalution*")
evaluation = model.evaluate_generator(
                generator=validation_generator(BATCH_SIZE),
                steps=BATCH_SIZE,
                verbose=1
                )
print(evaluation)

# Prediccion
# x_pred = x_train_e
# y_pred = model.predict(x_pred)

def print_predictions():
    print("*predictions*")
    for i in range(len(x_pred)):
        print("decision taken :")
        print(get_decision(y_pred[i]))
        print("solution:")
        print(y_train_e[i])
        print(" ")

# print_predictions()

import time
time.sleep(1)
FILE.close()
FILE_E.close()
