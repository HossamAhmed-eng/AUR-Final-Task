#include "gripper.h"

Gripper::Gripper(int servoPin, int openAngle, int closeAngle)
    : servoPin(servoPin), openAngle(openAngle), closeAngle(closeAngle) {}

void Gripper::init() {
    servo.attach(servoPin);
}

void Gripper::open() {
    servo.write(openAngle);
    Serial.println("👐 Gripper Opened");
}

void Gripper::close() {
    servo.write(closeAngle);
    Serial.println("✊ Gripper Closed");
}
