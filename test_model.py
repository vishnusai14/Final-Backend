from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

saved_model = load_model("./model")


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

train_data_prediction = saved_model.predict(input_vector_train).flatten()
print(output_vector_train)
train_data_result = pd.DataFrame(
    data={'Prediction By Model': train_data_prediction, 'Actual Model': output_vector_train})
print(train_data_result)
plt.plot(train_data_result['Prediction By Model'])
plt.plot(train_data_result['Actual Model'])
plt.show()
