from flask import Flask, jsonify, request, render_template
from datetime import datetime
from sample_logic import *

app = Flask(__name__)


@app.route("/api/v1", methods=['GET'])
def home():
    return jsonify({'result': 'App is Running'}), 201


@app.route("/api/v1/home", methods=['GET'])
def main():
    return render_template('sample.html')


@app.route("/api/v1/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        print("It is Post method")
        date = request.form.get('date')
        place = request.form.get('place')
        place = place.lower()
        format_date = datetime.strptime(
            date, "%Y-%m-%d").strftime('%m/%d/%Y')

        delT = get_prediction_result(format_date, place)
        return render_template("result.html", delT=delT)
