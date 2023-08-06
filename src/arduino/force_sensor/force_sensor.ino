#define FORCE_SENSOR_0 A0
#define FORCE_SENSOR_1 A1
#define FORCE_SENSOR_2 A2
#define FORCE_SENSOR_3 A3
#define FORCE_SENSOR_4 A4
#define LED_0 8
#define LED_1 9
#define LED_2 10
#define LED_3 11
#define LED_4 12

String LED_state;
int LED0, LED1, LED2, LED3, LED4;

void setup() {
  Serial.begin(9600);
  pinMode(LED_0,OUTPUT);
  pinMode(LED_1,OUTPUT);
  pinMode(LED_2,OUTPUT);
  pinMode(LED_3,OUTPUT);
  pinMode(LED_4,OUTPUT);
}

void loop() {
  int FS0_Reading = analogRead(FORCE_SENSOR_0);
  int FS1_Reading = analogRead(FORCE_SENSOR_1);
  int FS2_Reading = analogRead(FORCE_SENSOR_2);
  int FS3_Reading = analogRead(FORCE_SENSOR_3);
  int FS4_Reading = analogRead(FORCE_SENSOR_4);
  
  //-------------------------------------------------
  //print(FS0=0,FS1=0,FS2=0,FS3=0,FS4=0)
  //-------------------------------------------------
  Serial.print("FS0=");   
  Serial.print(FS0_Reading);
  Serial.print(",FS1=");   
  Serial.print(FS1_Reading);
  Serial.print(",FS2=");   
  Serial.print(FS2_Reading);
  Serial.print(",FS3=");   
  Serial.print(FS3_Reading);
  Serial.print(",FS4=");   
  Serial.println(FS4_Reading);
  
  //--------------------------------------------------------------------
  //按壓強度判斷 
  //print(FS0=NOTHING,FS1=NOTHING,FS2=NOTHING,FS3=NOTHING,FS4=NOTHING)
  //--------------------------------------------------------------------
  if (FS0_Reading < 50) {  
    Serial.print("FS0=NOTHING,");   
  }
  else if (FS0_Reading < 500) {
    Serial.print("FS0=HANGER,");
  }
  else{
    Serial.print("FS0=CLOTHES,");  
  }

  if (FS1_Reading < 50) {  
    Serial.print("FS1=NOTHING,");   
  }
  else if (FS1_Reading < 500) {
    Serial.print("FS1=HANGER,");
  }
  else{
    Serial.print("FS1=CLOTHES,");  
  }

  if (FS2_Reading < 50) {  
    Serial.print("FS2=NOTHING,");   
  }
  else if (FS2_Reading < 500) {
    Serial.print("FS2=HANGER,");
  }
  else{
    Serial.print("FS2=CLOTHES,");  
  }

  if (FS3_Reading < 50) {  
    Serial.print("FS3=NOTHING,");   
  }
  else if (FS3_Reading < 500) {
    Serial.print("FS3=HANGER,");
  }
  else{
    Serial.print("FS3=CLOTHES,");  
  }

  if (FS4_Reading < 50) {  
    Serial.println("FS4=NOTHING");   
  }
  else if (FS4_Reading < 500) {
    Serial.println("FS4=HANGER");
  }
  else{
    Serial.println("FS4=CLOTHES");  
  }

  //--------------------------------------------------------
  //LED狀態判斷 read(LED0=0,LED1=0,LED2=1,LED3=0,LED4=0)
  //--------------------------------------------------------
  while(Serial.available()>0){
    LED_state = Serial.readString();
    LED0 = LED_state.substring(5,6).toInt();
    LED1 = LED_state.substring(12,13).toInt();
    LED2 = LED_state.substring(19,20).toInt();
    LED3 = LED_state.substring(26,27).toInt();
    LED4 = LED_state.substring(33).toInt();

    digitalWrite(LED_0, LED0);  
    digitalWrite(LED_1, LED1);  
    digitalWrite(LED_2, LED2);  
    digitalWrite(LED_3, LED3);  
    digitalWrite(LED_4, LED4);
  }                      
  
  delay(50);
}
