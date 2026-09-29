from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "d55b760fb402a924acc8a4db23a48d4e"

PROJECT_ID = "2400ede70d2b"
TEMP_ID = "2224"
HUM_ID = "2225"


def get_data(parameter_id):
    url = f"https://www.thingsay.com/api/get/{PROJECT_ID}/{parameter_id}"

    params = {
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data")
def data():

    temperature = get_data(TEMP_ID)
    humidity = get_data(HUM_ID)

    return jsonify({
        "temperature": temperature,
        "humidity": humidity
    })


if __name__ == "__main__":
    app.run(debug=True)