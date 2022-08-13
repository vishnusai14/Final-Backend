import tensorflow as tf
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import *
from keras.callbacks import ModelCheckpoint
from keras.losses import MeanSquaredError
from keras.metrics import RootMeanSquaredError
from keras.optimizers import Adam
import matplotlib.pyplot as plt


def data_frame_to_input_output_vector(df, size=5):
    df_as_np = df.to_numpy()
    input_vector = []
    output_vector = []
    for i in range(len(df_as_np)-size):
        row = [[data] for data in df_as_np[i:i+size]]
        input_vector.append(row)
        label = df_as_np[i+size]
        output_vector.append(label)
    return np.array(input_vector), np.array(output_vector)


data_frame = pd.read_csv("./data/julyKavaratti.csv")
# print(data_frame.head())
data_frame.index = pd.to_datetime(data_frame['Timestamp'])
temperature_column = data_frame["DelT"]
input_vector, output_vector = data_frame_to_input_output_vector(
    temperature_column, 5)
input_vector_train, output_vector_train = input_vector[:2000], output_vector[:2000]
input_vector_validation, output_vector_validation = input_vector[
    2000:2558], output_vector[2000:2558]
input_vector_test, output_vector_test = input_vector[2559:], output_vector[2559:]
print(input_vector_train)
# model = Sequential()
# model.add(InputLayer((5, 1)))
# model.add(LSTM(64))
# model.add(Dense(8, 'relu'))
# model.add(Dense(1, 'linear'))

# # print(model.summary())

# save_model_callback = ModelCheckpoint("./model", save_best_only=True)

# # Compile The Model
# model.compile(loss=MeanSquaredError(), optimizer=Adam(
#     learning_rate=0.001), metrics=[RootMeanSquaredError()])
# model.fit(input_vector_train, output_vector_train, validation_data=(
#     input_vector_validation, output_vector_validation), epochs=50, callbacks=[save_model_callback])
