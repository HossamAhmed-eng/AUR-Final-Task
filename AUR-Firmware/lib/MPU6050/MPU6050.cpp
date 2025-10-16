#include "MPU6050.h"

void MPU::init(uint8_t address)
{
    addr = address;
    Wire.begin();
    Wire.setClock(400000); // Fast I2C mode

    // Wake up the MPU6050 (it starts in sleep mode)
    Wire.beginTransmission(addr);
    Wire.write(REG_PWR_MGMT_1);
    Wire.write(0x00);
    Wire.endTransmission();

    delay(100); // Give it time to stabilize
}

void MPU::configureGyro(uint16_t range)
{
    uint8_t fs_sel = 0;
    if (range == 250)
        fs_sel = 0;
    else if (range == 500)
        fs_sel = 1;
    else if (range == 1000)
        fs_sel = 2;
    else if (range == 2000)
        fs_sel = 3;

    Wire.beginTransmission(addr);
    Wire.write(REG_GYRO_CONFIG);
    Wire.write(fs_sel << 3);
    Wire.endTransmission();
}

void MPU::configureAccel(uint16_t range)
{
    uint8_t afs_sel = 0;
    if (range == 2)
        afs_sel = 0;
    else if (range == 4)
        afs_sel = 1;
    else if (range == 8)
        afs_sel = 2;
    else if (range == 16)
        afs_sel = 3;

    Wire.beginTransmission(addr);
    Wire.write(REG_ACCEL_CONFIG);
    Wire.write(afs_sel << 3);
    Wire.endTransmission();
}

void MPU::getGyroData(float *gx, float *gy, float *gz)
{
    Wire.beginTransmission(addr);
    Wire.write(REG_GYRO_XOUT_H);
    Wire.endTransmission(false);

    Wire.requestFrom(addr, 6, true);

    int16_t rawX = (Wire.read() << 8) | Wire.read();
    int16_t rawY = (Wire.read() << 8) | Wire.read();
    int16_t rawZ = (Wire.read() << 8) | Wire.read();

    *gx = (float)rawX;
    *gy = (float)rawY;
    *gz = (float)rawZ;
}
void MPU::getAccelData(float *ax, float *ay, float *az)
{
    Wire.beginTransmission(addr);
    Wire.write(REG_ACCEL_XOUT_H);
    Wire.endTransmission(false);

    Wire.requestFrom(addr, 6, true);

    int16_t rawX = (Wire.read() << 8) | Wire.read();
    int16_t rawY = (Wire.read() << 8) | Wire.read();
    int16_t rawZ = (Wire.read() << 8) | Wire.read();

    *ax = (float)rawX;
    *ay = (float)rawY;
    *az = (float)rawZ;
}


float MPU::getPitch(float ax, float ay, float az)
{
    return atan2(-ax, sqrt(ay*ay + az*az)) * 180.0 / PI;
}

float MPU::getRoll(float ax, float ay, float az)
{
    return atan2(ay, az) * 180.0 / PI;
}

float MPU::getYaw(float ax, float ay, float az)
{
    return atan2(sqrt(ax * ax + ay * ay), az) * 180.0 / PI;
}
