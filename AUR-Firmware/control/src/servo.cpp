#include "servo.h"

ServoMotor::ServoMotor(int pin, int minAngle, int maxAngle)
    : pin(pin), minAngle(minAngle), maxAngle(maxAngle), currentAngle(90) {}

void ServoMotor::init() {
    servo.attach(pin);
    servo.write(currentAngle); 
}

void ServoMotor::setAngle(int angle) {
    angle = constrain(angle, minAngle, maxAngle);
    servo.write(angle);
    currentAngle = angle;
}

void ServoMotor::rotateBy(int delta) { 
    int newAngle = constrain(currentAngle + delta, minAngle, maxAngle);
    servo.write(newAngle);
    currentAngle = newAngle;
}

int ServoMotor::getAngle() const {
    return currentAngle;
}



