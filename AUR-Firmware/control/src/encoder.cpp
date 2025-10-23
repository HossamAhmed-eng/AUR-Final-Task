#include "encoder.h"

Encoder::Encoder(int pinA, int pinB)
    : pinA(pinA), pinB(pinB),
      lastA(0), lastB(0),
      count(0), lastCount(0),
      lastTime(0), speed(0), direction(0) {}

void Encoder::init() {
    pinMode(pinA, INPUT_PULLUP);
    pinMode(pinB, INPUT_PULLUP);
    lastA = digitalRead(pinA);
    lastB = digitalRead(pinB);
    lastTime = micros();
}

void Encoder::update() {
    int currentA = digitalRead(pinA);
    int currentB = digitalRead(pinB);

    // detect change in A or B
    if (currentA != lastA || currentB != lastB) {
        // determine direction
        if (currentA == currentB)
            count++;
        else
            count--;

        // direction
        direction = (count >= lastCount) ? 1 : -1;
        lastCount = count;
    }

    // calculate speed every 50ms
    unsigned long now = micros();
    float dt = (now - lastTime) / 1e6;
    if (dt >= 0.05) { // 50ms
        long diff = count - lastCount;
        speed = diff / dt;
        lastTime = now;
        lastCount = count;
    }

    lastA = currentA;
    lastB = currentB;
}

long Encoder::getCount() const {
    return count;
}

float Encoder::getSpeed(float counts_per_rev) {
    float rev_per_sec = speed / counts_per_rev;
    return rev_per_sec * 2 * PI; // rad/s
}

float Encoder::getPosition(float counts_per_rev) {
    return (count / counts_per_rev) * 360.0; // degrees
}

float Encoder::getRPM(float counts_per_rev) {
    float rev_per_sec = speed / counts_per_rev;
    rpmValue = rev_per_sec * 60.0;
    return rpmValue;
}

int Encoder::getDirection() const {
    return direction;
}
