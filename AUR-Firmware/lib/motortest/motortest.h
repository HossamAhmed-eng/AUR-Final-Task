#pragma once
#include <Arduino.h>
#include <ESP32Encoder.h>
#include "pid.h"

class MotorDriver
{
public:
    MotorDriver(int in1, int in2, int ena, int in3, int in4, int enb);
    void begin(int leftEncA, int leftEncB, int rightEncA, int rightEncB, float ticksPerRev);

    void setTargetRPM(double left, double right);
    void update();
    void stop();

    void moveForward();
    void moveBackward();
    void turnLeft();
    void turnRight();
    void stopMotors();

private:
    int in1, in2, ena;
    int in3, in4, enb;
    float ticksPerRev;

    double targetLeftRPM;
    double targetRightRPM;

    unsigned long lastUpdate;
    long prevLeftTicks;
    long prevRightTicks;

    ESP32Encoder leftEnc;
    ESP32Encoder rightEnc;

    PID leftPID;
    PID rightPID;
};
