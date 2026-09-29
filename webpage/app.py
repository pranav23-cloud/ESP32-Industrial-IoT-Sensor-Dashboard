from flask import Flask, jsonify, render_template
import serial
import json
import requests
import threading
import time
import os

app = Flask(__name__)

# -----------------------------
# ESP32 SERIAL SETTINGS
# -----------------------------
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

# -----------------------------
# THINGSAY SETTINGS
# -----------------------------
PROJECT_ID = "a3ac8aab8f6b"

TEMPERATURE_ID = "2226"
HUMIDITY_ID = "2227"
DISTANCE_ID = "2228"

API_KEY = os.getenv("THINGSAY_API_KEY")

# -----------------------------
# LATEST SENSOR DATA
# -----------------------------
latest_data = {
    "temperature": None,
    "humidity": None,
    "distance": None,
    "timestamp": None,
    "online": False
}

lock = threading.Lock()


# -----------------------------
# SEND DATA TO THINGSAY
# -----------------------------
def send_to_thingsay(parameter_id, value):

    if not API_KEY:
        print("ERROR: THINGSAY_API_KEY is not set")
        return

    url = (
        f"https://www.thingsay.com/api/send/"
        f"{PROJECT_ID}/{parameter_id}/{value}"
        f"?key={API_KEY}"
    )

    try:

        response = requests.post(url, timeout=10)

        print(
            f"ThingSay | Parameter: {parameter_id} "
            f"| Value: {value} "
            f"| Status: {response.status_code}"
        )

        # PRINT THINGSAY RESPONSE
        print("ThingSay response:", response.text)

    except requests.RequestException as e:

        print("ThingSay error:", e)


# -----------------------------
# READ ESP32 SERIAL DATA
# -----------------------------
def serial_worker():

    while True:

        try:

            print(f"Connecting to {SERIAL_PORT}...")

            with serial.Serial(
                SERIAL_PORT,
                BAUD_RATE,
                timeout=2
            ) as ser:

                print("ESP32 Connected!")

                with lock:
                    latest_data["online"] = True

                while True:

                    line = (
                        ser.readline()
                        .decode("utf-8", errors="ignore")
                        .strip()
                    )

                    if not line:
                        continue

                    # Ignore anything that isn't JSON
                    if not line.startswith("{"):
                        continue

                    print("Received:", line)

                    try:

                        data = json.loads(line)

                        temperature = float(data["temperature"])
                        humidity = float(data["humidity"])
                        distance = float(data["distance"])

                    except (
                        json.JSONDecodeError,
                        KeyError,
                        TypeError,
                        ValueError
                    ):

                        print("Invalid JSON received")
                        continue

                    # -----------------------------
                    # UPDATE BACKEND DATA
                    # -----------------------------
                    with lock:

                        latest_data["temperature"] = temperature
                        latest_data["humidity"] = humidity
                        latest_data["distance"] = distance

                        latest_data["timestamp"] = time.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                        latest_data["online"] = True

                    # -----------------------------
                    # SEND TO THINGSAY
                    # -----------------------------
                    send_to_thingsay(
                        TEMPERATURE_ID,
                        temperature
                    )

                    send_to_thingsay(
                        HUMIDITY_ID,
                        humidity
                    )

                    if distance >= 0:

                        send_to_thingsay(
                            DISTANCE_ID,
                            distance
                        )

        except serial.SerialException as e:

            print("Serial error:", e)

            with lock:
                latest_data["online"] = False

            print("Retrying in 3 seconds...")
            time.sleep(3)

        except Exception as e:

            print("Backend error:", e)

            with lock:
                latest_data["online"] = False

            time.sleep(3)


# -----------------------------
# WEBPAGE
# -----------------------------
@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# SENSOR API
# -----------------------------
@app.route("/api/sensors")
def sensors():

    with lock:
        return jsonify(latest_data)


# -----------------------------
# START APPLICATION
# -----------------------------
if __name__ == "__main__":

    # Start ESP32 serial reader
    thread = threading.Thread(
        target=serial_worker,
        daemon=True
    )

    thread.start()

    # Start Flask server
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )