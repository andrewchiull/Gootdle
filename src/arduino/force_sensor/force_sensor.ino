#define FORCE_SENSOR_0 A0
#define LED_0 13

void setup() {
  Serial.begin(9600);
  pinMode(LED_0,OUTPUT);
  pinMode(FORCE_SENSOR_0,INPUT);
}

void loop() {
  int FS0_Reading = analogRead(FORCE_SENSOR_0);
  Serial.println(FS0_Reading);

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "1 ON") {
      
    }
    Serial.print("You sent me: ");
    Serial.println(data);
  }
  
  delay(50);
}
