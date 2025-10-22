#include "kalman_filter.h"
#include <math.h>

KalmanFilter::KalmanFilter(float wr, float wb, float tpr)
{
    wheel_radius = wr;
    wheel_base = wb;
    ticks_per_rev = tpr;
    pos_x = pos_y = heading = 0;

    P[0][0] = 1.0;
    P[0][1] = 0.0;
    P[1][0] = 0.0;
    P[1][1] = 1.0;

    Q[0][0] = 0.01;
    Q[0][1] = 0.0;
    Q[1][0] = 0.0;
    Q[1][1] = 0.01;
  
    R[0][0] = 0.1;
    R[0][1] = 0.0;
    R[1][0] = 0.0;
    R[1][1] = 0.1;
}

bool KalmanFilter::begin(uint8_t mpu_addr)
{
    mpu.init(mpu_addr);
    return true;
}

void KalmanFilter::update(float left_ticks, float right_ticks, float dt)
{
    float gx, gy, gz;
    mpu.getGyroData(&gx, &gy, &gz);

    float left_dist = (left_ticks / ticks_per_rev) * (2 * M_PI * wheel_radius);
    float right_dist = (right_ticks / ticks_per_rev) * (2 * M_PI * wheel_radius);

    float distance = (left_dist + right_dist) / 2.0;
    float encoder_turn = (right_dist - left_dist) / wheel_base;
    float imu_turn = gz * dt;

    float fused_turn = (encoder_turn * 1 + imu_turn * 0);

    heading += fused_turn;
    pos_x += distance * cos(heading);
    pos_y += distance * sin(heading);

    P[0][0] += Q[0][0];
    P[1][1] += Q[1][1];
}

void KalmanFilter::correct(float measured_x, float measured_y)
{
    float K_x = P[0][0] / (P[0][0] + R[0][0]);
    float K_y = P[1][1] / (P[1][1] + R[1][1]);

    pos_x += K_x * (measured_x - pos_x);
    pos_y += K_y * (measured_y - pos_y);

    P[0][0] *= (1 - K_x);
    P[1][1] *= (1 - K_y);
}

void KalmanFilter::getPosition(float &x, float &y, float &h)
{
    x = pos_x;
    y = pos_y;
    h = heading;
}

void KalmanFilter::setPosition(float x, float y, float h)
{
    pos_x = x;
    pos_y = y;
    heading = h;

    P[0][0] = 1.0;
    P[1][1] = 1.0;
}