#ifndef ENCODER_H
#define ENCODER_H

#include <Arduino.h>

class Encoder {
private:
    int pinA, pinB;
    volatile long count;  //pulse count
    long lastCount;
    unsigned long lastTime;
    float speed;  // counts per second
    float rpmValue; // revolutions per minute
    int direction; // 1 = forward, -1 = backward
public:
    Encoder(int pinA, int pinB);
    void init(uint8_t index); //initialize with index for multiple encoders
    void update();
    long getCount() const;
    float getSpeed(float counts_per_rev); //rad/s
    float getPosition(float counts_per_rev); //degrees
    float getRPM(float counts_per_rev); //RPM
     int getDirection() const; 
};
//interrupt handlers
void IRAM_ATTR handleEncoderA0();
void IRAM_ATTR handleEncoderA1();
#endif
