from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Concatenate # Merge
from keras.layers.merge import concatenate
from keras.optimizers import Adam

def nn(n_input_layers, input_info, return_tensors=False):

    # Input layers
    #inputs = []
    #inputs_layers = [];
    merge_layer_size = 0

    for i in range(n_input_layers):
        #inpt = Input(shape=(input_info[i]['m'],))
        #input_layer = Dense(int(1.00 * input_info[i]['m']),
        #                    input_shape=(input_info[i]['m'],),
        #                    activation='relu')(inpt)
        #inputs.append(inpt)
        #inputs_layers.append(input_layer)

        merge_layer_size = merge_layer_size + input_info["input"][i]['m']

    #print("merge_layer_size:", merge_layer_size)
    # Merge Layer
    #merge = concatenate(inputs_layers)

    input2 = Input(shape=(merge_layer_size,))

    # Hidden layer
    hidden_layer_size = int(merge_layer_size * 1.75)
    hidden_layer = Dense(hidden_layer_size, activation='relu')(input2)

    # Output Layer
    output_size = 8
    output_layer = Dense(output_size, activation='softmax')(hidden_layer)

    # Compile
    optimizer = Adam(lr=0.001) # default lr = 0.001

    model = Model(inputs=input2, outputs=output_layer)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    if return_tensors:
        return model, input2, output_layer

    return model

'''
Notes

# Dropout Layer
model.add(Dropout(0.5))

'''
