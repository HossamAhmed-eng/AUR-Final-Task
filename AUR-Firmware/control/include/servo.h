#ifndef SERVO_H
#define SERVO_H

#include <Arduino.h>
#include <Servo.h>

class ServoMotor {
private:
    Servo servo;       
    int pin;           
    int currentAngle;   
    int minAngle;      
    int maxAngle;        

public:
    ServoMotor(int pin, int minAngle = 0, int maxAngle = 180);

    void init();                   
    void setAngle(int angle);    // absolute angle  
    void rotateBy(int delta);  // relative rotation     
    int getAngle() const;  // return current angle    
                 
};

#endif
