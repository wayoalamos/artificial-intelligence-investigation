import keras
import numpy as np
# from test import test

def conver_matrix_for_model(matrix):
    # convert matrix 4x4 to data_type for NN model
    complete_string = ""
    for i in range(4):
        for j in range(4):
            num = matrix[i][j]
            complete_string += '0'*num + '1' + '0'*(15-num)
    return np.array([list(complete_string)]).astype('f')


model = keras.models.load_model('15puzzle_solver_model.h5')


state = [[1,0,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
state = conver_matrix_for_model(state)
# we can expect the model to suggest a left move of the 0
# that means that the first element of prediction must be the highest

prediction = model.predict(state) # probability of moving 0 to [left, down, right, up]
print(prediction)

state = [[4,1,2,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]]
state = conver_matrix_for_model(state)
# we can expect the model to suggest a left move of the 0
# that means that the fourth element of prediction must be the highest

prediction = model.predict(state)
print(prediction)

# test(model)
