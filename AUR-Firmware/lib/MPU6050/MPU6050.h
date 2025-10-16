#ifndef MPU6050_H
#define MPU6050_H
#include <Arduino.h>
#include <Wire.h>

// MPU6050 Register Map
#define REG_WHO_AM_I 0x75
#define REG_PWR_MGMT_1 0x6B
#define REG_SMPLRT_DIV 0x19
#define REG_CONFIG 0x1A
#define REG_GYRO_CONFIG 0x1B
#define REG_ACCEL_CONFIG 0x1C
#define REG_INT_ENABLE 0x38
#define REG_ACCEL_XOUT_H 0x3B
#define REG_GYRO_XOUT_H 0x43
#define REG_TEMP_OUT_H 0x41
struct MPU
{
private:
    uint8_t addr; // device address (encapsulated)

public:
    // initialization
    void init(uint8_t address);

    // configuration
    void configureGyro(uint16_t range);
    void configureAccel(uint16_t range);

    // sensor data
    void getGyroData(float *gx, float *gy, float *gz);
    void getAccelData(float *ax, float *ay, float *az);

    // orientation
    float getPitch(float ax, float ay, float az);
    float getRoll(float ax, float ay, float az);
    float getYaw(float ax, float ay, float az);
};

#endif // MPU6050_H