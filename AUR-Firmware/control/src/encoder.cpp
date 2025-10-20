#include "encoder.h"
#include "Arduino.h"
static Encoder* encoders[2] = {nullptr, nullptr};

//interrupt handlers
void IRAM_ATTR handleEncoderA0() {
    if (encoders[0] == nullptr) return;
    int b = digitalRead(encoders[0]->pinB);
    if (b == HIGH){  // forward
        encoders[0]->count++;
        encoders[0]->direction = 1;  
     } 
    else{ // backward
        encoders[0]->count--;
        encoders[0]->direction =-1;  
}}

void IRAM_ATTR handleEncoderA1() {
    if (encoders[1] == nullptr) return;
    int b = digitalRead(encoders[1]->pinB);
    if (b == HIGH){// forward
        encoders[1]->count++;
      encoders[1]->direction = 1;
       }   
    else{  // backward
        encoders[1]->count--;
        encoders[1]->direction = -1;   
}}

//class
Encoder::Encoder(int pinA, int pinB)
    : pinA(pinA), pinB(pinB), count(0), lastCount(0), lastTime(0), speed(0) {}

void Encoder::init(uint8_t index) {
    pinMode(pinA, INPUT_PULLUP);
    pinMode(pinB, INPUT_PULLUP);
    encoders[index] = this;
    if (index == 0)
        attachInterrupt(digitalPinToInterrupt(pinA), handleEncoderA0, RISING);
    else if (index == 1)
        attachInterrupt(digitalPinToInterrupt(pinA), handleEncoderA1, RISING);
    lastTime = micros();  //microseconds
}

void Encoder::update() {
    unsigned long now = micros();
    float dt = (now - lastTime) / 1e6;
    if (dt >= 0.05) { //50ms
        long diff = count - lastCount;
        speed = diff / dt;
        lastCount = count;
        lastTime = now;
    }
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