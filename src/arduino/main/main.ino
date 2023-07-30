#include <Servo.h>

// Ultrasonic pins
#define buzzer 2
#define TRIGPIN_1 A2
#define ECHOPIN_1 A1
#define TRIGPIN_2 13
#define ECHOPIN_2 12

// Motor pins
#define L_F 11  // Left Forward
#define L_B 10
#define R_F 5
#define R_B 6  // Right Backward


// Claw
#define MID 90    // Initial angle
#define RANGE 30  // Grabbing angle

Servo servoL;
Servo servoR;

// Temperature
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN A4     // Digital pin connected to the DHT sensor
#define DHTTYPE    DHT11     // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;


float L_MAX = 255;  // Left Forward MAX
float R_MAX = 255;  // Right Forward MAX
float speed = 0.8;
boolean is_opened = false;
boolean isReadingTemperature = false;
boolean isReadingDistance = false;
boolean isBeep = true;
float DELAY_TIME = 100;

void setup() {
    // put your setup code here, to run once:

    pinMode(L_F, OUTPUT);
    pinMode(L_B, OUTPUT);
    pinMode(R_F, OUTPUT);
    pinMode(R_B, OUTPUT);

    pinMode(TRIGPIN_1, OUTPUT);
    pinMode(ECHOPIN_1, INPUT);
    pinMode(TRIGPIN_2, OUTPUT);
    pinMode(ECHOPIN_2, INPUT);

    servoL.attach(9);
    servoR.attach(3);

    Serial.begin(9600);
    // Initialize device.
    dht.begin();
    // Print temperature sensor details.
    sensor_t sensor;
    dht.temperature().getSensor(&sensor);
    delayMS = sensor.min_delay / 1000;

}

void stepForward() {
    Serial.println("stepForward");
    forward();
    delay(DELAY_TIME);
    stop();
}


void stepBackward() {
    Serial.println("stepBackward");
    backward();
    delay(DELAY_TIME);
    stop();
}


void forward() {
    Serial.println("Go forward");
    analogWrite(L_F, L_MAX * speed);
    analogWrite(L_B, 0);
    analogWrite(R_F, R_MAX * speed);
    analogWrite(R_B, 0);
}

void backward() {
    Serial.println("Go backward");
    analogWrite(L_F, 0);
    analogWrite(L_B, L_MAX * speed);
    analogWrite(R_F, 0);
    analogWrite(R_B, R_MAX * speed);
}

void left() {
    Serial.println("Go left");
    analogWrite(L_F, 0);
    analogWrite(L_B, L_MAX * speed * 0.8);
    analogWrite(R_F, R_MAX * speed * 0.8);
    analogWrite(R_B, 0);
    delay(DELAY_TIME);
    stop();
}

void right() {
    Serial.println("Go right");
    analogWrite(L_F, L_MAX * speed * 0.8);
    analogWrite(L_B, 0);
    analogWrite(R_F, 0);
    analogWrite(R_B, R_MAX * speed * 0.8);
    delay(DELAY_TIME);
    stop();
}

void stop() {
    Serial.println("Stop motor");
    analogWrite(L_F, 0);
    analogWrite(L_B, 0);
    analogWrite(R_F, 0);
    analogWrite(R_B, 0);
}

void readUltra() {
    digitalWrite(TRIGPIN_1, LOW);  // Set the trigger pin to low for 2us
    delayMicroseconds(2);
    digitalWrite(TRIGPIN_1, HIGH);  // Send a 10uS high to trigger ranging
    delayMicroseconds(10);
    digitalWrite(TRIGPIN_1, LOW);             // Send pin low again
    int distance = pulseIn(ECHOPIN_1, HIGH);  // Read in times pulse
    distance = distance / 58;               // Calculate distance (in cm) from time of pulse
//    Serial.println(distance);
    delay(50);
    if (distance < 18) {
        buzzerbeep();
    }
}

void buzzerbeep() {
    Serial.println("Too close!");
    tone(buzzer, 1000);  // Send 1KHz sound signal...
    delay(DELAY_TIME / 2);
    noTone(buzzer);
}

void readDistance() {
    digitalWrite(TRIGPIN_2, LOW);  // Set the trigger pin to low for 2us
    delayMicroseconds(2);
    digitalWrite(TRIGPIN_2, HIGH);  // Send a 10uS high to trigger ranging
    delayMicroseconds(10);
    digitalWrite(TRIGPIN_2, LOW);             // Send pin low again
    int distance = pulseIn(ECHOPIN_2, HIGH);  // Read in times pulse
    distance = distance / 58;               // Calculate distance (in cm) from time of pulse
    Serial.println(distance);
    delay(500);
}


void readTemperature() {
  // Delay between measurements.
  delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));
  }
}

void open() {
    if (is_opened) {
        Serial.println("Already opened!");
        return;
    }
    is_opened = true;
    Serial.println("Open");
    for (int i = 0; i <= RANGE; i += 1) {
        servoL.write(MID + i);
        servoR.write(MID - i);
        delay(50);
    }
}

void close() {
    if (!is_opened) {
        Serial.println("Already closed!");
        return;
    }
    is_opened = false;
    Serial.println("Close");
    for (int i = 0; i <= RANGE; i += 1) {
        servoL.write(MID + RANGE - i);
        servoR.write(MID - RANGE + i);
        delay(50);
    }
}

void setSpeed(float num) {
    speed = num;
    Serial.println(speed);
}

void loop() {

    if (millis() % 2000 < 100 && isBeep) {
      readUltra();
      }

    if (isReadingTemperature) {
        readTemperature();
    }
    if (isReadingDistance) {
        readDistance();
    }
    if (Serial.available() == 0) {
        return;
    }

    String data = Serial.readStringUntil('\n');
    Serial.print("[ECHO] ");
    Serial.println(data);

    if (data == "forward") {
        forward();
        delay(DELAY_TIME * 3);
        stop();
    } else if (data == "backward") {
        backward();
        delay(DELAY_TIME * 3);
        stop();
    } else if (data == "left") {
        left();
    } else if (data == "right") {
        right();
    } else if (data == "open") {
        open();
    } else if (data == "close") {
        close();
    } else if (data == "stop") {
        stop();
    } else if (data == "stepForward") {
        stepForward();
    } else if (data == "stepBackward") {
        stepBackward();
    } else if (data == "tempon") {
        isReadingTemperature = true;
    } else if (data == "tempoff") {
        isReadingTemperature = false;
    } else if (data == "diston") {
        isReadingDistance = true;
    } else if (data == "distoff") {
        isReadingDistance = false;
    } else if (data == "beepon") {
        isBeep = true;
    } else if (data == "beepoff") {
        isBeep = false;
    } else {
        setSpeed(data.toFloat());
    }
}
