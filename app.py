from flask import Flask, jsonify, request, render_template
from datetime import datetime
from sample_logic import *
from createCsv import *

app = Flask(__name__)


@app.route("/api/v1", methods=['GET'])
def home():
    return jsonify({'result': 'App is Running'}), 201


@app.route("/api/v1/home", methods=['GET'])
def main():
    return render_template('sample.html')


@app.route("/api/v1/test", methods=['POST'])
def test():
    if request.method == 'POST':
        coordinate = request.json.get('coordinate')
        print(coordinate)


@app.route("/api/v1/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        print(request.json)
        print("It is Post method")
        date = request.json.get('date')
        cor = request.json.get('cor')
        print(cor)
        rounded_lat = round(cor['latitude'], 2)
        rounded_long = round(cor['longitude'], 2)

        createCsv(rounded_lat, rounded_long)
        place = str(rounded_lat) + "-" + str(rounded_long)

        print(place)

        delT = get_prediction_result(date, place)
        power_freshwater_dict = {"18": ['56', '1.24'], "19": [
            '63', '1.3'], "20": ['70', '1.36'], "21": ['77', '1.43']}

        if (delT == 'Enter Date within a week'):
            return 'Enter Date within a week'
        else:
            delTtoString = ""
            if (delT < 18.5):
                delTtoString = str(18)
            elif (delT > 18.5 and delT <= 19.5):
                delTtoString = str(19)
            elif (delT > 19.5 and delT <= 20.5):
                delTtoString = str(20)
            elif (delT > 20.5):
                delTtoString = str(21)

            power_fresh_water = power_freshwater_dict[delTtoString]
            print(power_fresh_water)

            return power_fresh_water


if __name__ == "__main__":
    app.run(host='192.168.43.254', port=3000, debug=True)
