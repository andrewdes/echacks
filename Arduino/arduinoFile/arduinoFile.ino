#include <Servo.h>

//Servo variables
const int servoPin = 8; //pin number
const int maxpos = 180; //maximum position
const int minpos = 10; //minimum position
const int distance = 3; //distance each keypress moves servo
const int dly = 500; //delay
int pos = 90; 

//Servo2 variables
const int s2dly = 70; //stepper delay
const int servoPin2 = 7;
const int s2Stop = 90;
const int s2Left = 180;
const int s2Right = 0;

Servo servo;  
Servo servo2;
 
void setup()
{
  Serial.begin(9600);  
  servo.attach(servoPin);
  servo2.attach(servoPin2);
  servo.write(pos);
}//end setup
 
 
void loop()
{
  if (Serial.available()){
    char input = Serial.read();
    if (input == 'w'){
      if (pos <=  (maxpos - distance)){
        pos -= distance;
        servo.write(pos);
        delay(dly);
      }     
    }else if (input == 's'){
      if (pos >= (minpos + distance)){
        pos += distance;
        servo.write(pos);
        delay(dly); 
      }//end if pos     
    }else if (input == 'd'){
      servo2.s2Right(0);
      delay(s2dly);
      servo2.write(s2Stop);
      delay(s2dly);
    }else if (input == 'a'){
      servo2.write(s2Left);
      delay(s2dly);
      servo2.write(s2Stop);
      delay(s2dly);
    }//end if input   

      
  }//end if serial
}//end loop
