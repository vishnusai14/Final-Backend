#### Only delT is predicted still freshwater and power generation need to be calculated ###
#### That has to be done based on the NIOT plant situated in different co-ordinate given value ####


import pandas as pd
from datetime import datetime, timedelta
from keras.models import load_model

data_frame = pd.read_csv("./data/julyKavaratti.csv")
final_date = data_frame.iloc[-1]['Timestamp']

# Get in this Format from the User
date_to_predict = '22-7-2020 10:30 AM'
date_to_predict_string = date_to_predict

final_date = datetime.strptime(final_date, '%d-%m-%Y %I:%M %p')
date_to_predict = datetime.strptime(date_to_predict, '%d-%m-%Y %I:%M %p')
latest_date = final_date

date_differ = (date_to_predict-final_date).days

if date_differ < 0:
    print("Data is Already There")
    delT = (data_frame.loc[data_frame['Timestamp']
                           == date_to_predict_string]['DelT'].values)[0]
    print("The Predicted DelT for " + str(date_to_predict) + " is : " +
          str(delT))

elif abs(date_differ) > 7:
    print("Enter Date within a week")

else:
    # Do the Prediction
    saved_model = load_model("./model")
    hour_differ = (final_date-date_to_predict).total_seconds() / (60*60)
    no_of_time_prediction_to_happen = abs(hour_differ) / 6
    # for i in range(0, no_of_time_prediction_to_happen):
    last_five_result = [[[a]
                        for a in data_frame.tail()['DelT'].to_numpy().flatten()]]
    for i in range(0, int(no_of_time_prediction_to_happen)):
        train_data_prediction = saved_model.predict(last_five_result).flatten()
        latest_date = final_date + timedelta(hours=(6*(i+1)))
        latest_date = datetime.strftime(latest_date, '%d-%m-%Y %I:%M %p')
        print(latest_date)

        df = pd.DataFrame({'Timestamp': [str(latest_date)], 'SST(K)': ['NaN'], 'CW(K)': [
                          '282'], 'DelT': [train_data_prediction.tolist()[0]]})

        df.to_csv('./data/julyKavaratti.csv',
                  mode='a', index=False, header=False)
        # print(last_five_result)

        # Update the last_five_result
        last_five_result[0].pop(0)
        last_five_result[0].append(train_data_prediction.tolist())
        print(last_five_result)

    print("The Predicted DelT for " + str(date_to_predict) + " is : " +
          str(last_five_result[0][len(last_five_result)-1][0]))
