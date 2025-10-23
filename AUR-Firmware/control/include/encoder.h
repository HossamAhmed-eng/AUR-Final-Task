#ifndef ENCODER_H
#define ENCODER_H

#include <Arduino.h>

class Encoder {
private:
    int pinA, pinB;
    int lastA, lastB;
    long count;           // Pulse count
    long lastCount;
    unsigned long lastTime;
    float speed;          // counts per second
    float rpmValue;       // revolutions per minute
    int direction;        // 1 = forward, -1 = backward

public:
    Encoder(int pinA, int pinB);
    void init();
    void update();  // must be called frequently in loop()
    long getCount() const;
    float getSpeed(float counts_per_rev);   // rad/s
    float getPosition(float counts_per_rev); // degrees
    float getRPM(float counts_per_rev);     // RPM
    int getDirection() const;
};

#endif
