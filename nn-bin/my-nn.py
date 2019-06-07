# load
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Concatenate # Merge
from keras.layers.merge import concatenate
from keras.optimizers import Adam
from load import load_data, load_evaluation_data


# training
import os
os.environ["THEANO_FLAGS"] = "device=cpu,floatX=float32,mode=FAST_RUN,allow_gc=False"
from keras.utils.vis_utils import plot_model
import numpy as np

FILE_NAME = "model_diagram"

# load
def load_nn(n_input_layers, n_hidden_layers, n_output_layers):
    # Creates the NN model, then return it.

    # Input layer
    input = Input(shape = (n_input_layers,))

    # Hidden layer
    hidden_layer = Dense(units=16, activation='relu')(input)
    #hidden_layer = Dense(units=16*5, activation='relu')(hidden_layer)
    #hidden_layer = Dense(units=16, activation='relu')(hidden_layer)

    # Output layer
    output_layer = Dense(units=n_output_layers, activation='softmax')(hidden_layer)

    model = Model(inputs=input, outputs=output_layer)

    # Compile
    optimizer = Adam()
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model

# training
def nn_read_samples(n):
    global index
    if index > len(x_train):
        index = 0
    x_sample = x_train[index:index+n]
    y_sample = y_train[index:index+n]
    index += n
    return [x_sample, y_sample]

def nn_read_evaluation_samples(n):
    global index_e
    if index_e > len(x_train_e):
        index_e = 0
    x_sample_e = x_train_e[index_e:index_e+n]
    y_sample_e = y_train_e[index_e:index_e+n]
    index_e += n
    return [x_sample_e, y_sample_e]

def generator(batch_size):
    while 1:
        yield nn_read_samples(batch_size)

def validation_generator(batch_size):
    while 1:
        yield nn_read_evaluation_samples(batch_size)

def evaluate_generator(batch_size):
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


model = load_nn(16*16,16*10,4)
plot_model(model, to_file=(FILE_NAME + '.png'), show_shapes=True)
#model.summary()

x_train, y_train = load_data()
x_train_e, y_train_e = load_evaluation_data()

index = 0
index_e = 0

BATCH_SIZE = 50
STEPS_PER_EPOCH = int(len(x_train)/BATCH_SIZE) # cuantos batches tomo por epoch -> ideal : total/batchsize
VALIDATION_STEPS = int(len(x_train_e)/BATCH_SIZE)

model.fit_generator(
                epochs=100,
                generator=generator(BATCH_SIZE),
                steps_per_epoch=STEPS_PER_EPOCH, # cambiar
                validation_data=validation_generator(BATCH_SIZE),
                validation_steps=VALIDATION_STEPS,
                verbose=1
                )

print("*evalution*")
evaluation = model.evaluate_generator(
                generator=evaluate_generator(BATCH_SIZE),
                steps=BATCH_SIZE,
                verbose=1
                )

print(evaluation)

# Prediccion
x_pred = x_train_e
y_pred = model.predict(x_pred)

def print_predictions():
    print("*predictions*")
    for i in range(len(x_pred)):
        print("decision taken :")
        print(get_decision(y_pred[i]))
        print("solution:")
        print(y_train_e[i])
        print(" ")

# print_predictions()
