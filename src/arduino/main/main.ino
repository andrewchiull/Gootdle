// [How to format simple string? - Using Arduino / Programming Questions - Arduino Forum](https://forum.arduino.cc/t/how-to-format-simple-string/927426/13)
#include <ArduinoJson.h>

#define FORCE_SENSOR_0 A0 // Testing
#define LED_0 13 // Build-in LED

#define SLOTS_SIZE 5
#define FORCE_SENSOR_1 A0
#define LED_1 8

float DELAY_TIME = 100;
DynamicJsonDocument doc(1024);

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    while (!Serial) continue;
    Serial.println("CONNECTION_MADE");

    pinMode(LED_0, OUTPUT);
    pinMode(FORCE_SENSOR_0, INPUT);

    for (int i = 0; i < SLOTS_SIZE; i++) {
        pinMode(LED_1+i, OUTPUT);
        pinMode(FORCE_SENSOR_1+i, INPUT);
    }
    
    while (true) {
        if (Serial.available() == 0) continue;
        String data = Serial.readStringUntil('\n');
        Serial.print("Arduino received: ");
        Serial.println(data);
        break;
    }


}

void loop() {
    // Run unless received command
    if (Serial.available() == 0) return; 

    String data = Serial.readStringUntil('\n');
    Serial.print("Arduino received: ");
    Serial.println(data);

    deserializeJson(doc, data);


    auto sender = doc["sender"];
    auto command = doc["command"];

    if (command == "read_sensors") {
        // read and send data to RPi
        Serial.println("Read sensors");

        auto sensors = doc["sensors"];
        sensors[0] = analogRead(LED_0);
        for (int i = 0; i < SLOTS_SIZE; i++) {
            sensors[1+i] = analogRead(LED_1 + i);
        }

    }

    sender = "arduino";
    serializeJson(doc, Serial);
    Serial.println();
    delay(DELAY_TIME);
}
