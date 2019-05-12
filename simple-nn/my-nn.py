# load
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Concatenate # Merge
from keras.layers.merge import concatenate
from keras.optimizers import Adam

# training
import os
os.environ["THEANO_FLAGS"] = "device=cpu,floatX=float32,mode=FAST_RUN,allow_gc=False"
from keras.utils.vis_utils import plot_model
import numpy as np

model_file = "model_diagram"

# load
def load_nn(n_input_layers, n_hidden_layers, n_output_layers):

    # Input layer
    input = Input(shape = (n_input_layers,))

    # Hidden layer
    hidden_layer = Dense(units=n_hidden_layers, activation='relu')(input)
    hidden_layer = Dense(units=n_hidden_layers, activation='relu')(hidden_layer)
    hidden_layer = Dense(units=n_hidden_layers, activation='relu')(hidden_layer)
    hidden_layer = Dense(units=n_hidden_layers, activation='relu')(hidden_layer)

    # Output layer
    output_layer = Dense(units=n_output_layers, activation='sigmoid')(hidden_layer)

    model = Model(inputs=input, outputs=output_layer)

    # Compile
    optimizer = Adam()
    model.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])

    return model

# training
print("Creating a NN model...")
model = load_nn(2,10,1)

plot_model(model, to_file=(model_file + '.png'), show_shapes=True)


# generator, validation_generator, training_size, validation_size = load.get_generator(batch_size, validation_split=0.01)

model.summary()

x_train, y_train = np.array(
    [[3,10],[4,5],[2,10],[10,2],[9,8],[10,8],[13,12],[1,5]]),np.array(
    [0,0,0,1,1,1,1,0])

#model.fit(x=x_train, y=y_train, epochs=1000, batch_size=5)

model.fit_generator(generator, epochs=1000)

def see_weights(model):
    for capa in model.layers:
        print("weights: ", capa.get_weights())

see_weights(model)
# x_test, y_test = np.array([3]), np.array([6])

# Prediccion
x_pred = np.array([[41,41],[5,5],[8,8],[2,2],[4,2],[12,5],[61,1]])
y_pred = model.predict(x_pred)

print("*predictions*")
print(x_pred)
print(y_pred)
