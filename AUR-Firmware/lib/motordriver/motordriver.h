#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H

#include <Arduino.h>

class MotorDriver
{
public:
    // Constructor (takes all pin numbers)
    MotorDriver(int in1, int in2, int ena, int in3, int in4, int enb);

    // Setup and control
    void begin();
    void moveForward();
    void moveBackward();
    void turnLeft();
    void turnRight();
    void stopMotors();
    void setSpeed(int speedValue);

private:
    // Motor pins
    int _IN1, _IN2, _ENA;
    int _IN3, _IN4, _ENB;

    // PWM
    int _pwmChannelA = 0;
    int _pwmChannelB = 1;
    int _freq = 1000;
    int _resolution = 8;

    // Current speed (0–255)
    int _motorSpeed = 200;
};

#endif
