#include "motor.h"

Motor::Motor(int pwmPin, int dirPin1, int dirPin2, int pwmChannel, int pwmfreq, int resolution)
    : pwmPin(pwmPin), dirPin1(dirPin1), dirPin2(dirPin2),
      pwmchannel(pwmChannel), pwmfreq(pwmfreq), resolution(resolution), currentDirection(0) {}

void Motor::init() {
    pinMode(dirPin1, OUTPUT);
    pinMode(dirPin2, OUTPUT);
    ledcSetup(pwmchannel, pwmfreq, resolution);
    ledcAttachPin(pwmPin, pwmchannel);
}

void Motor::setSpeed(float speed) {
    speed = constrain(speed, -100, 100);

    if (speed > 0) {
        setDirection(true);
    } else if (speed < 0) {
        setDirection(false);
    } else {
        stop();
        return;
    }

    int duty = map(abs(speed), 0, 100, 0, (1 << resolution) - 1);
    ledcWrite(pwmchannel, duty);
}

void Motor::setDirection(bool forward) {
    if (forward) {   
        digitalWrite(dirPin1, HIGH);
        digitalWrite(dirPin2, LOW);
        currentDirection = 1;
    } else {
        digitalWrite(dirPin1, LOW);
        digitalWrite(dirPin2, HIGH);
        currentDirection = -1;
    }
}

int Motor::getDirection() const {
    return currentDirection;
}

void Motor::stop() {
    digitalWrite(dirPin1, LOW);
    digitalWrite(dirPin2, LOW);
    ledcWrite(pwmchannel, 0);
    currentDirection = 0;
}
