#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

#define TRIG_PIN 5
#define ECHO_PIN 18

DHT dht(DHTPIN, DHTTYPE);

float readDistance()
{
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH, 30000);

    if (duration == 0)
    {
        return -1;
    }

    float distance = duration * 0.0343 / 2;

    return distance;
}

void setup()
{
    Serial.begin(115200);

    dht.begin();

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop()
{
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    float distance = readDistance();

    if (isnan(temperature) || isnan(humidity))
    {
        delay(5000);
        return;
    }

    // Send ONLY JSON to Python
    Serial.print("{");

    Serial.print("\"temperature\":");
    Serial.print(temperature, 2);

    Serial.print(",\"humidity\":");
    Serial.print(humidity, 2);

    Serial.print(",\"distance\":");
    Serial.print(distance, 2);

    Serial.println("}");

    delay(5000);
}