````markdown
# DHT11 AND ESP32 IoT PROJECT

## DHT11 Temperature & Humidity Monitoring Using ESP32

This project demonstrates how to collect temperature and humidity data using a **DHT11 sensor connected to an ESP32** and send the data to the **ThingSay IoT platform**.

The project contains two different approaches:

1. **ESP32 + Python + MQTT**
2. **ESP32 + Wi-Fi + REST API without Python**

It also includes a **Flask Web Dashboard** for displaying the sensor data.

---

## PROJECT OVERVIEW

The DHT11 sensor measures:

- Temperature
- Humidity

The ESP32 reads the sensor values and sends them to ThingSay.

The project demonstrates different IoT communication architectures and helps understand the difference between using an intermediate Python application and communicating directly from the ESP32.

---

# HARDWARE USED

| Component | Purpose |
|---|---|
| ESP32 | Microcontroller and Wi-Fi communication |
| DHT11 | Temperature and humidity sensor |
| USB Cable | ESP32 programming and serial communication |
| Computer | Python and development |
| Wi-Fi | Internet communication |

---

# DHT11 CONNECTION

| DHT11 | ESP32 |
|---|---|
| VCC | 3.3V |
| DATA | GPIO 4 |
| GND | GND |

The DHT11 DATA pin is connected to **GPIO 4**.

---

# METHOD 1 — USING PYTHON + MQTT

### Architecture

```text
DHT11
   ↓
ESP32
   ↓
USB / Serial
   ↓
Python
   ↓
MQTT
   ↓
ThingSay
````

### How it works

1. DHT11 measures temperature and humidity.
2. ESP32 reads the sensor values.
3. ESP32 sends the values through Serial/USB.
4. Python reads the Serial data.
5. Python processes the data.
6. Python publishes the data using MQTT.
7. ThingSay receives and stores the data.

### Technologies

* ESP32
* DHT11
* Python
* PySerial
* MQTT
* ThingSay

### Install Python libraries

```bash
pip install pyserial paho-mqtt requests
```

---

# METHOD 2 — WITHOUT PYTHON

In this method, Python is removed from the sensor-to-cloud communication path.

The ESP32 connects directly to Wi-Fi and sends data to ThingSay using HTTPS REST API.

### Architecture

```text
DHT11
   ↓
ESP32
   ↓
Wi-Fi
   ↓
HTTPS REST API
   ↓
ThingSay
```

### How it works

1. DHT11 measures temperature and humidity.
2. ESP32 reads the sensor values.
3. ESP32 connects to Wi-Fi.
4. ESP32 sends the sensor data directly to ThingSay.
5. ThingSay stores the data.

Python is not required for sending the sensor data.

---

# WEB DASHBOARD

The project also includes a web dashboard that displays the latest temperature and humidity values.

### Dashboard Architecture

```text
DHT11
   ↓
ESP32
   ↓
Wi-Fi
   ↓
ThingSay
   ↓
REST API
   ↓
Flask Backend
   ↓
HTML + CSS + JavaScript
   ↓
Web Dashboard
```

The dashboard displays:

* Temperature
* Humidity
* Last updated time
* System status

The webpage automatically requests new sensor data every **5 seconds**.

---

# THINGSAY API

ThingSay is used as the IoT cloud platform for storing and retrieving sensor data.

### Project

```text
Project ID: 2400ede70d2b
```

### Parameters

```text
Temperature → 2224
Humidity    → 2225
```

### Fetch Temperature

```text
GET /api/get/2400ede70d2b/2224
```

### Fetch Humidity

```text
GET /api/get/2400ede70d2b/2225
```

Example response:

```json
{
    "parameter_id": 2224,
    "value": "31.00",
    "timestamp": "2026-09-29T13:03:11.980511"
}
```

---

# WEB DASHBOARD STRUCTURE

```text
WEB_DASHBOARD/
│
├── app.py
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

### app.py

Flask backend that communicates with the ThingSay API.

### index.html

Contains the dashboard structure.

### style.css

Contains the dashboard design and styling.

---

# API KEY SECURITY

The ThingSay API key should **not** be stored directly in the source code.

The Flask application uses an environment variable:

```python
import os

API_KEY = os.getenv("THINGSAY_API_KEY")
```

Set the API key in PowerShell:

```powershell
$env:THINGSAY_API_KEY="YOUR_API_KEY"
```

The API key is not included in this repository.

---

# RUN THE WEB DASHBOARD

Navigate to the dashboard folder:

```powershell
cd WEB_DASHBOARD
```

Set the ThingSay API key:

```powershell
$env:THINGSAY_API_KEY="YOUR_API_KEY"
```

Run the Flask application:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

in your browser.

---

# COMPARISON

| Feature      | With Python | Without Python |
| ------------ | ----------- | -------------- |
| ESP32        | Yes         | Yes            |
| DHT11        | Yes         | Yes            |
| Python       | Yes         | No             |
| MQTT         | Yes         | No             |
| REST API     | No          | Yes            |
| USB Serial   | Yes         | No             |
| Direct Wi-Fi | No          | Yes            |
| ThingSay     | Yes         | Yes            |

### With Python

```text
ESP32 → Serial → Python → MQTT → ThingSay
```

### Without Python

```text
ESP32 → Wi-Fi → REST API → ThingSay
```

---

# SOFTWARE AND TECHNOLOGIES

* Arduino IDE
* ESP32
* DHT11
* Python
* Flask
* MQTT
* REST API
* HTTP/HTTPS
* HTML
* CSS
* JavaScript
* ThingSay
* Git
* GitHub

---

# WHAT I LEARNED

Through this project, I learned:

* DHT11 sensor interfacing
* ESP32 programming
* GPIO
* Serial communication
* Wi-Fi communication
* MQTT
* REST APIs
* HTTP/HTTPS requests
* ThingSay IoT platform
* Python data processing
* Flask
* HTML
* CSS
* JavaScript
* API authentication
* Environment variables
* Git and GitHub
* IoT cloud communication

---

# PROJECT FLOW

## Using Python

```text
        DHT11
          ↓
        ESP32
          ↓
       Serial
          ↓
        Python
          ↓
        MQTT
          ↓
       ThingSay
```

## Without Python

```text
        DHT11
          ↓
        ESP32
          ↓
        Wi-Fi
          ↓
    HTTPS REST API
          ↓
       ThingSay
```

## Web Dashboard

```text
        DHT11
          ↓
        ESP32
          ↓
        Wi-Fi
          ↓
       ThingSay
          ↓
       REST API
          ↓
    Flask Backend
          ↓
   HTML + CSS + JS
          ↓
    Web Dashboard
```

---

# FUTURE IMPROVEMENTS

* Real-time sensor graphs
* Historical data visualization
* Multiple sensors
* Temperature and humidity alerts
* Mobile-friendly dashboard
* Database integration
* User authentication
* Cloud deployment
* Real-time MQTT dashboard
* Automatic device monitoring

---

# AUTHOR

**Pranav Patil**

GitHub:

[https://github.com/pranav23-cloud](https://github.com/pranav23-cloud)

---

## LICENSE

This project is created for learning, experimentation, and IoT development.

```
```
