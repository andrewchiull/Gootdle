// [How to format simple string? - Using Arduino / Programming Questions - Arduino Forum](https://forum.arduino.cc/t/how-to-format-simple-string/927426/13)
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>

#define FORCE_SENSOR_0 A0
#define LED_0 13 // Build-in LED for testing

#define SLOTS_SIZE 5
#define LED_STRAND_PIN 6

// memory calculator [Assistant | ArduinoJson 6](https://arduinojson.org/v6/assistant/#/step1)
#define DOC_SIZE 512 // Don't go to large or small

float DELAY_TIME = 10;

String data;

void read_line() {
    Serial.print("[[ECHO]]");
    data = Serial.readStringUntil('\n');
    Serial.println(data);
}

Adafruit_NeoPixel led_strand;


// Reference: EasyNeoPixels.h created by Evelyn Masso, April 9, 2017.

void setup_led_strand(int pin, int num) {
  led_strand = Adafruit_NeoPixel(num, pin, NEO_GRB + NEO_KHZ800);
  led_strand.begin();
}

// set the nth neopixel to a particular brightness of white
// meant to be used with val as HIGH or LOW
void write_led_strand(int num, int val) {
  led_strand.setPixelColor(num, led_strand.Color(val*255,val*255,val*255));
  led_strand.show();
}

// set the nth neopixel to a particular rgb color
void write_led_strand(int num, int r, int g, int b) {
  led_strand.setPixelColor(num, led_strand.Color(r,g,b));
  led_strand.show();
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
    read_line();
    // [Step 5] Server starts to send messages


    pinMode(LED_0, OUTPUT);
    pinMode(FORCE_SENSOR_0, INPUT);

    for (int i = 0; i <= SLOTS_SIZE; i++) {
        pinMode(FORCE_SENSOR_0+i, INPUT);
    }

    setup_led_strand(LED_STRAND_PIN, SLOTS_SIZE);

}

void loop() {
    bool received = (Serial.available() > 0);
    // Run if received command
    if (received) {
        read_line();

        // // test
        // DynamicJsonDocument doc(DOC_SIZE);
        // deserializeJson(doc, data);
        // doc["sender"] = "test";
        // serializeJson(doc, Serial);
        // Serial.println();
    }

    // Parse data string to json
    DynamicJsonDocument doc(DOC_SIZE);
    deserializeJson(doc, data);

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

        // int leds_test[] = {0,0,1,1,0,0};
        // Write LED
        Serial.print("[[DEBUG]]");
        for (int i = 0; i <= SLOTS_SIZE; i++) {

            // Serial.print(leds_test[i]);
            // write_led_strand(i, leds_test[i]);
            Serial.print(int(leds[i]));
            write_led_strand(i, int(leds[i]));
        }
        Serial.println();
    }

    // Respond
    if (received) {
        doc["sender"] = "arduino";
        serializeJson(doc, Serial);
        Serial.println();
    }




    // doc.clear();
    delay(DELAY_TIME);
}
