#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

class Motor {
private:
    int pwmPin;
    int dirPin1;
    int dirPin2;
    int pwmchannel;    
    int pwmfreq;       
    int resolution;  
    int currentDirection;

public:
    Motor(int pwmPin, int dirPin1, int dirPin2, int pwmChannel, int pwmfreq = 20000, int resolution = 10);

    void init();
    void setSpeed(float speed); 
    void setDirection(bool forward);
    int getDirection() const;
    void stop();
};
    
#endif
