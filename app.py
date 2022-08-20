import math
from re import L
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

        rounded_lat_difff = rounded_lat - math.floor(rounded_lat)
        rounded_lat_difff = round(rounded_lat_difff, 2)

        rounded_long_difff = rounded_long - math.floor(rounded_long)
        rounded_long_difff = round(rounded_long_difff, 2)

        print("This is the rounded_diff", rounded_lat_difff, rounded_long_difff)

        final_lat = 0
        final_long = 0
        if rounded_lat_difff < 0.25:
            final_lat = math.floor(rounded_lat)
        elif rounded_lat >= 0.25 and rounded_lat < 0.5:
            final_lat = math.floor(rounded_lat) + 0.25
        elif rounded_lat >= 0.5 and rounded_lat < 0.75:
            final_lat = math.floor(rounded_lat) + 0.25
        elif rounded_lat >= 0.75 and rounded_lat < 1:
            final_lat = math.floor(rounded_lat) + 0.75
        else:
            final_lat = math.floor(rounded_lat) + 1

        if rounded_long_difff < 0.25:
            final_long = math.floor(rounded_long)
        elif rounded_long >= 0.25 and rounded_long < 0.5:
            final_long = math.floor(rounded_long) + 0.25
        elif rounded_long >= 0.5 and rounded_long < 0.75:
            final_long = math.floor(rounded_long) + 0.25
        elif rounded_long >= 0.75 and rounded_long < 1:
            final_long = math.floor(rounded_long) + 0.75

        else:
            final_long = math.floor(rounded_long) + 1
        correct_place = createCsv(final_lat, final_long)
        if correct_place:
            place = str(final_lat) + "-" + str(final_long)

            print("This is the place : ",  place)

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
        else:
            return "Please Select Correct Region"


if __name__ == "__main__":
    app.run(host='192.168.43.254', port=3000, debug=True)
