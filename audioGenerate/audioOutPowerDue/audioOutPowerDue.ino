#include <Wire.h>
#include <WM8731_Audio.h>

float curFreq = 2000.0;


void setup(void) {
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);

  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);


  Codec.begin();
  Codec.setOutputVolume(110); // 0 - 127
  Codec.playTone(curFreq);
  //Codec.halt();
}

void loop()
{

}
