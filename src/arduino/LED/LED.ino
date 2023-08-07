/*

Blink bright white light from a single Neopixel!

*/

#include <EasyNeoPixels.h>

String msg;
int LED[5];

void setup() {
    // setup for one NeoPixel attached to pin 13
    setupEasyNeoPixels(6, 5);
    Serial.begin(9600);
}

void loop() {
    // turn the NeoPixel ON
    while(Serial.available()){
      msg = Serial.readString();
      for (int i=0;i<5;i++){
        LED[i] = msg.substring(5+(7*i),6+(7*i)).toInt();
      }
      for (int i=0;i<5;i++){
        writeEasyNeoPixel(i, LED[i]);
      }
    }
}
