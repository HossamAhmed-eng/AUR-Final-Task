#include "motortest.h"

MotorDriver::MotorDriver(int in1, int in2, int ena, int in3, int in4, int enb)
    : in1(in1), in2(in2), ena(ena),
      in3(in3), in4(in4), enb(enb),
      ticksPerRev(0),
      targetLeftRPM(0), targetRightRPM(0),
      lastUpdate(0), prevLeftTicks(0), prevRightTicks(0),
      leftPID(1.0, 0.3, 0.05, 255),
      rightPID(1.0, 0.3, 0.05, 255) {}

void MotorDriver::begin(int leftEncA, int leftEncB, int rightEncA, int rightEncB, float ticksPerRev)
{
    this->ticksPerRev = ticksPerRev;

    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);

    ledcSetup(0, 1000, 8);
    ledcSetup(1, 1000, 8);
    ledcAttachPin(ena, 0);
    ledcAttachPin(enb, 1);

    leftEnc.attachHalfQuad(leftEncA, leftEncB);
    rightEnc.attachHalfQuad(rightEncA, rightEncB);
    //ESP32Encoder::useInternalWeakPullResistors = UP;
}

void MotorDriver::setTargetRPM(double left, double right)
{
    targetLeftRPM = left;
    targetRightRPM = right;
}

void MotorDriver::update()
{
    unsigned long now = millis();
    double dt = (now - lastUpdate) / 1000.0;
    if (dt < 0.05)
        return;

    long leftTicks = leftEnc.getCount();
    long rightTicks = rightEnc.getCount();

    double leftSpeed = (leftTicks - prevLeftTicks) / ticksPerRev / dt * 60.0;
    double rightSpeed = (rightTicks - prevRightTicks) / ticksPerRev / dt * 60.0;

    double leftOut = leftPID.get_output(targetLeftRPM, leftSpeed);
    double rightOut = rightPID.get_output(targetRightRPM, rightSpeed);

    digitalWrite(in1, leftOut > 0);
    digitalWrite(in2, leftOut <= 0);
    digitalWrite(in3, rightOut > 0);
    digitalWrite(in4, rightOut <= 0);

    ledcWrite(0, fabs(leftOut));
    ledcWrite(1, fabs(rightOut));

    prevLeftTicks = leftTicks;
    prevRightTicks = rightTicks;
    lastUpdate = now;
}

void MotorDriver::stop()
{
    stopMotors();
}

void MotorDriver::moveForward()
{
    setTargetRPM(150, 150);
}

void MotorDriver::moveBackward()
{
    setTargetRPM(-150, -150);
}

void MotorDriver::turnLeft()
{
    setTargetRPM(-100, 100);
}

void MotorDriver::turnRight()
{
    setTargetRPM(100, -100);
}

void MotorDriver::stopMotors()
{
    setTargetRPM(0,0);
    ledcWrite(0, 0);
    ledcWrite(1, 0);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
}
