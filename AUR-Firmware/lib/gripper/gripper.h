#ifndef GRIPPER_H
#define GRIPPER_H

#include <Arduino.h>
#include <ESP32Servo.h>

class Gripper {
private:
    int servoPin;
    int openAngle;
    int closeAngle;
    Servo servo;

public:
    Gripper(int servoPin, int openAngle = 0, int closeAngle = 90);
    void init();
    void open();
    void close();
};

#endif
