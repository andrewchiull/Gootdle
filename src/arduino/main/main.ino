// [How to format simple string? - Using Arduino / Programming Questions - Arduino Forum](https://forum.arduino.cc/t/how-to-format-simple-string/927426/13)
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>

#define FORCE_SENSOR_0 A0
#define LED_0 13 // Build-in LED for testing

#define SLOTS_SIZE 5
#define LED_STRAND_PIN 6

// memory calculator [Assistant | ArduinoJson 6](https://arduinojson.org/v6/assistant/#/step1)
#define DOC_SIZE 512 // Don't go to large or small

#define DELAY_TIME 100

// LED_0 is unused
Adafruit_NeoPixel pixels(SLOTS_SIZE + 1, LED_STRAND_PIN, NEO_GRB + NEO_KHZ800);



// // Reference: EasyNeoPixels.h created by Evelyn Masso, April 9, 2017.

// set the nth neopixel to a particular brightness of white
// meant to be used with val as HIGH or LOW
void write_led_strand(int num, int val) {
  pixels.setPixelColor(num, pixels.Color(val*255,val*255,val*255));
  pixels.show();
}

// set the nth neopixel to a particular rgb color
void write_led_strand(int num, int r, int g, int b) {
  pixels.setPixelColor(num, pixels.Color(r,g,b));
  pixels.show();
}


void setup() {
    Serial.begin(9600);

    // Wait until serial connection is made
    while (!Serial) continue;

    // [Step 1] Arduino responds that ARDUINO_IS_READY
    Serial.println("ARDUINO_IS_READY");

    // [Step 2] Server waits until ARDUINO_IS_READY
    // [Step 3] Server responds that SERVER_IS_READY

    // [Step 4] Arduino waits until server is ready
    while (Serial.available() == 0) continue;
    // update();
    // [Step 5] Server starts to send messages


    pinMode(LED_0, OUTPUT);
    pinMode(FORCE_SENSOR_0, INPUT);

    for (int i = 0; i <= SLOTS_SIZE; i++) {
        pinMode(FORCE_SENSOR_0+i, INPUT);
    }

    pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
}

void loop() {

    if (Serial.available() > 0) {

        // Parse data string to json
        DynamicJsonDocument doc(DOC_SIZE);
        DeserializationError err = deserializeJson(doc, Serial);

        Serial.print("[[ECHO]]");
        serializeJson(doc, Serial);
        Serial.println();

        if (err == DeserializationError::Ok) {

            String command = doc["command"];
            auto sensors = doc["sensors"];
            auto leds = doc["leds"];

            // TODO use Status design pattern
            if (command == "read_sensors") {
                for (int i = 0; i <= SLOTS_SIZE; i++) {
                    sensors[i] = analogRead(FORCE_SENSOR_0 + i);
                }
            }
            else if (command == "write_leds") {
                pixels.clear(); // Reset
                Serial.print("[[DEBUG]]write_leds:");
                for (int i = 1; i <= SLOTS_SIZE; i++) {
                    Serial.print(int(leds[i]));
                    write_led_strand(i, int(leds[i]));
                }
                Serial.println();
            }

            // Respond
            doc["sender"] = "arduino";
            serializeJson(doc, Serial);
            Serial.println();
        }
    }

    while (Serial.available() > 0)
        Serial.read();

    delay(DELAY_TIME);
}
