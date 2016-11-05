#include <Servo.h>

Servo servo;  

const int servoPin = 7; //pin number
const int maxpos = 180; //maximum position
const int minpos = 10; //minimum position
const int distance = 10; //distance each keypress moves servo
const int dly = 500; //delay
int pos = 10; 

 
void setup()
{
  Serial.begin(9600);  
  servo.attach(servoPin);
  servo.write(pos);
}//end setup
 
 
void loop()
{
  if (Serial.available()){
    char input = Serial.read();
    if (input == 'w'){
      if (pos <=  (maxpos - distance)){
        pos += distance;
        servo.write(pos);
        delay(dly);
      }     
    }else if (input == 's'){
      if (pos >= (minpos + distance)){
        pos -= distance;
        servo.write(pos);
        delay(dly); 
      }//end if pos     
    }//end if input    
  }//end if serial
}//end loop
