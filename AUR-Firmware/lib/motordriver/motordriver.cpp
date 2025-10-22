#include "MotorDriver.h"

MotorDriver::MotorDriver(int in1, int in2, int ena, int in3, int in4, int enb)
    : _IN1(in1), _IN2(in2), _ENA(ena),
      _IN3(in3), _IN4(in4), _ENB(enb) {}

void MotorDriver::begin()
{
    pinMode(_IN1, OUTPUT);
    pinMode(_IN2, OUTPUT);
    pinMode(_IN3, OUTPUT);
    pinMode(_IN4, OUTPUT);

    // Setup PWM channels
    ledcSetup(_pwmChannelA, _freq, _resolution);
    ledcSetup(_pwmChannelB, _freq, _resolution);

    // Attach pins to PWM
    ledcAttachPin(_ENA, _pwmChannelA);
    ledcAttachPin(_ENB, _pwmChannelB);

    stopMotors();
}

void MotorDriver::setSpeed(int speedValue)
{
    _motorSpeed = constrain(speedValue, 0, 255);
}

void MotorDriver::moveForward()
{
    digitalWrite(_IN1, HIGH);
    digitalWrite(_IN2, LOW);
    digitalWrite(_IN3, HIGH);
    digitalWrite(_IN4, LOW);
    ledcWrite(_pwmChannelA, _motorSpeed);
    ledcWrite(_pwmChannelB, _motorSpeed);
}

void MotorDriver::moveBackward()
{
    digitalWrite(_IN1, LOW);
    digitalWrite(_IN2, HIGH);
    digitalWrite(_IN3, LOW);
    digitalWrite(_IN4, HIGH);
    ledcWrite(_pwmChannelA, _motorSpeed);
    ledcWrite(_pwmChannelB, _motorSpeed);
}

void MotorDriver::turnLeft()
{
    // Left motor backward, right motor forward
    digitalWrite(_IN1, LOW);
    digitalWrite(_IN2, HIGH);
    digitalWrite(_IN3, HIGH);
    digitalWrite(_IN4, LOW);
    ledcWrite(_pwmChannelA, _motorSpeed);
    ledcWrite(_pwmChannelB, _motorSpeed);
}

void MotorDriver::turnRight()
{
    // Left motor forward, right motor backward
    digitalWrite(_IN1, HIGH);
    digitalWrite(_IN2, LOW);
    digitalWrite(_IN3, LOW);
    digitalWrite(_IN4, HIGH);
    ledcWrite(_pwmChannelA, _motorSpeed);
    ledcWrite(_pwmChannelB, _motorSpeed);
}

void MotorDriver::stopMotors()
{
    digitalWrite(_IN1, LOW);
    digitalWrite(_IN2, LOW);
    digitalWrite(_IN3, LOW);
    digitalWrite(_IN4, LOW);
    ledcWrite(_pwmChannelA, 0);
    ledcWrite(_pwmChannelB, 0);
}
