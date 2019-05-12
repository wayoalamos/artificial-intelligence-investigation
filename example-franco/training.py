import os
os.environ["THEANO_FLAGS"] = "device=cpu,floatX=float32,mode=FAST_RUN,allow_gc=False"
#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras.utils.vis_utils import plot_model
import keras
import numpy as np
import sys
from shutil import copyfile

import load, nn
from tf_utils import save_tf_model

from keras import backend as K

# Parse parameters
input_file = ''
model_file = ''
n_epoch    = 50
batch_size = 32

for i in range(len(sys.argv)):
    if sys.argv[i] == '-m':
        model_file = sys.argv[i + 1]
    elif sys.argv[i] == '-i':
        input_file = sys.argv[i + 1]
    elif sys.argv[i] == '-e':
        n_epoch = int(sys.argv[i + 1])
    elif sys.argv[i] == '-b':
        batch_size = int(sys.argv[i + 1])

if input_file == '':
    input_file = model_file

if model_file == '':
    model_file = input_file

if input_file != model_file:
    copyfile(input_file, model_file)


path_trained_model = model_file + '.h5'

if model_file == '':
    print('Model file is required.\n -m model_file')
    sys.exit()

print("BATCH SIZE: " + str(batch_size))
print("input: " + input_file);
print("output: " + model_file);




# Load data
input_info = load.load_nn_data(input_file)
n_input_layers = len(input_info)

print(n_input_layers)

# Model
if '-r' in sys.argv:
    print("Creating a NN model...")
    model = nn.nn(n_input_layers, input_info)
else:
    print('Loading existing model...')
    model = load_model(input_file + '.h5')

plot_model(model, to_file=(model_file + '.png'), show_shapes=True)

# Callbacks
class saveAll(keras.callbacks.Callback):
    def __init__(self, model_file_name):
        self.file  = model_file_name
        self.saved = []
        self.bound = 800 #-np.Inf

    def on_epoch_end(self, epoch, logs={}):
        current = logs.get('val_acc')
        percentage = int(current * 1000)

        if self.bound < percentage:
            if percentage not in self.saved:
                self.saved.append(percentage)
                self.bound = percentage 
                new_model = self.file + '_' + str(percentage)
                self.model.save_weights(new_model + '.h5', overwrite=True)
                copyfile(self.file, new_model)
                scripts.nn_to_txt.convert(new_model)

class saveLogs(keras.callbacks.Callback):
    def __init__(self, model_file_name):
        self.file = model_file_name
        self.best = -np.Inf

    def on_epoch_end(self, epoch, logs={}):
        if self.best < logs.get('val_acc'):
            self.best = logs.get('val_acc')

            with open(self.file + '_logs.txt', 'w') as f:
                f.write('val_acc: ' + str(logs.get('val_acc')) + '\n')
                f.write('acc: ' + str(logs.get('acc')) + '\n')
                f.write('loss: ' + str(logs.get('loss')) + '\n')
                f.write('\n')

class saveBestPb(keras.callbacks.Callback):
    def __init__(self, model, model_file_name):
        self.model = model
        self.file = model_file_name
        self.best = -np.Inf

    def on_epoch_end(self, epoch, log={}):
        current = log.get('val_acc')

        if self.best < current:
            self.best = current
            save_tf_model(self.model, self.file)


# Save
if '-s' in sys.argv:
    checkpoint1 = ModelCheckpoint(path_trained_model, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    checkpoint2 = saveAll(model_file)
    checkpoint4 = saveLogs(model_file)
    checkpoint5 = saveBestPb(model, model_file)
    callbacks_list = [checkpoint1, checkpoint4, checkpoint5] # checkpoint2, checkpoint3, checkpoint3

else:
    callbacks_list = []

generator, validation_generator, training_size, validation_size = load.get_generator(batch_size, validation_split=0.01)


steps_per_epoch = int(np.ceil(training_size / batch_size))
validation_steps = int(np.ceil(validation_size / batch_size))

model.summary()
model.fit_generator(epochs=n_epoch,
                    
                    generator=generator,
                    steps_per_epoch=steps_per_epoch,
                    
                    validation_data=validation_generator,
                    validation_steps=validation_steps,
                    
                    callbacks=callbacks_list,
                    #pickle_safe=False ???
                    )

#scripts.nn_to_txt.convert(model_file)

