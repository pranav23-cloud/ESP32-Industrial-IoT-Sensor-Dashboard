#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <DHT.h>

#define DHT_PIN 4
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

const char* ssid = "Abhyudyaya Tech 2.4G";
const char* password = "ATS@1124";

const char* host = "www.thingsay.com";

const char* apiKey = "d55b760fb402a924acc8a4db23a48d4e";
const char* projectId = "2400ede70d2b";

const int temperatureParamId = 2224;
const int humidityParamId = 2225;

WiFiClientSecure client;

void sendToThingSay(int parameterId, float value) {

  String url = "/api/send/";
  url += projectId;
  url += "/";
  url += parameterId;
  url += "/";
  url += String(value, 2);
  url += "?key=";
  url += apiKey;

  Serial.println("Sending:");
  Serial.println(url);

  if (client.connect(host, 443)) {

    // ThingSay requires POST
    client.println("POST " + url + " HTTP/1.1");
    client.println("Host: " + String(host));
    client.println("Connection: close");
    client.println("Content-Length: 0");
    client.println();

    // Read response
    while (client.connected()) {
      String line = client.readStringUntil('\n');

      if (line == "\r") {
        break;
      }

      Serial.println(line);
    }

    client.stop();

  } else {
    Serial.println("ThingSay connection failed");
  }
}

void setup() {

  Serial.begin(115200);

  dht.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);

  Serial.print("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi connected!");

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // For HTTPS
  client.setInsecure();

  Serial.println("DHT11 + ThingSay started");
}

void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {

    Serial.println("DHT11 READ ERROR");

    delay(2000);
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %RH");

  // Send temperature
  sendToThingSay(temperatureParamId, temperature);

  delay(1000);

  // Send humidity
  sendToThingSay(humidityParamId, humidity);

  Serial.println("----------------------");

  delay(5000);
}