
#include <Stepper.h>
#define STEPS_PER_MOTOR_REVOLUTION 32   
#define STEPS_PER_OUTPUT_REVOLUTION 32 * 64  

const int pin1 = 8;
const int pin2 = 9;
const int pin3 = 10;
const int pin4 = 11;
const int spd = 1000; //speed
const int dly = 200; //delay
const int revolution = 10; //1/10th of a revolution every time button is pressed
int  Steps2Take;

Stepper small_stepper(STEPS_PER_MOTOR_REVOLUTION, pin1, pin3, pin2, pin4);

void setup()   
{
  Serial.begin(9600);
}

void loop()   
{

  if (Serial.available()){
    char input = Serial.read();

    if(input == 'd'){
        Serial.println("clockwise");
        Steps2Take  =  STEPS_PER_OUTPUT_REVOLUTION / revolution;
        small_stepper.setSpeed(spd);   
        small_stepper.step(Steps2Take);
        delay(dly);
    }
    else if(input == 'a'){
        Serial.println("counter");
        Steps2Take  =  - STEPS_PER_OUTPUT_REVOLUTION / revolution;  
        small_stepper.setSpeed(spd);  
        small_stepper.step(Steps2Take);
        delay(dly);
    }
  }


}


