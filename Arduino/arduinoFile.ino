#include <Servo.h>
#include <Stepper.h>
#define STEPS_PER_MOTOR_REVOLUTION 32
#define STEPS_PER_OUTPUT_REVOLUTION 32 * 64

//Servo variables
const int servoPin = 7; //pin number
const int maxpos = 180; //maximum position
const int minpos = 10; //minimum position
const int distance = 10; //distance each keypress moves servo
const int dly = 500; //delay
int pos = 10; 

//Stepper variables
const int pin1 = 8;
const int pin2 = 9;
const int pin3 = 10;
const int pin4 = 11;
const int spd = 1000; //speed
const int stepDly = 200; //stepper delay
const int revolution = 20; // 1/20th of a revolution 
int Steps2Take;

Servo servo;  
Stepper stepper(STEPS_PER_MOTOR_REVOLUTION, pin1, pin3, pin2, pin4);
 
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
    }else if (input == 'd'){
        Steps2Take  =  STEPS_PER_OUTPUT_REVOLUTION / revolution;
        stepper.setSpeed(spd);   
        stepper.step(Steps2Take);
        delay(stepDly);
    }else if (input == 'a'){
        Steps2Take  =  - STEPS_PER_OUTPUT_REVOLUTION / revolution;  
        stepper.setSpeed(spd);  
        stepper.step(Steps2Take);
        delay(stepDly);
    }
    

      
  }//end if serial
}//end loop
