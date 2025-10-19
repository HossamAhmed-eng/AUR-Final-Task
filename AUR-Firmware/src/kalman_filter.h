#ifndef KALMAN_FILTER_H
#define KALMAN_FILTER_H

#include "MPU6050.h"

class KalmanFilter
{
private:
    float pos_x, pos_y, heading;
    float P[2][2]; // covariance matrix
    float Q[2][2]; // process noise
    float R[2][2]; // measurement noise

    MPU mpu;
    float wheel_radius, wheel_base, ticks_per_rev;

public:
    KalmanFilter(float wr, float wb, float tpr);
    bool begin(uint8_t mpu_addr = 0x68);
    void update(float left_ticks, float right_ticks, float dt);
    void correct(float measured_x, float measured_y);
    void getPosition(float &x, float &y, float &h);
    void setPosition(float x, float y, float h = 0);
};

#endif