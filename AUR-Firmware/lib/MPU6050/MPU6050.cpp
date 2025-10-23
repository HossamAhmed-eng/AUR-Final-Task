#include "MPU6050.h"

void MPU::init(uint8_t address)
{
    addr = address;
    Wire.begin(4,16);
    Wire.setClock(400000); // Fast I2C mode

    // Wake up the MPU6050 (it starts in sleep mode)
    Wire.beginTransmission(addr);
    Wire.write(REG_PWR_MGMT_1);
    Wire.write(0x00);
    Wire.endTransmission();

    delay(100); // Give it time to stabilize
    
    // Configure default ranges
    configureGyro(250);  // ±250°/s
    configureAccel(2);   // ±2g
    
    // Perform calibration
    calibrateMPU6050();
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

// Get calibrated gyro data
void MPU::getCalibratedGyroData(float *gx, float *gy, float *gz)
{
    getGyroData(gx, gy, gz);
    
    // Apply calibration offsets
    *gx -= gyroOffsetX;
    *gy -= gyroOffsetY;
    *gz -= gyroOffsetZ;
}

// Get calibrated accelerometer data
void MPU::getCalibratedAccelData(float *ax, float *ay, float *az)
{
    getAccelData(ax, ay, az);
    
    // Apply calibration offsets
    *ax -= accelOffsetX;
    *ay -= accelOffsetY;
    *az -= accelOffsetZ;
}

// Calibration function
void MPU::calibrateMPU6050()
{
    const int numSamples = 500; // Number of samples for calibration
    const int delayTime = 10;   // Delay between samples in ms
    
    float gyroSumX = 0, gyroSumY = 0, gyroSumZ = 0;
    float accelSumX = 0, accelSumY = 0, accelSumZ = 0;
    
    Serial.println("Calibrating MPU6050... Keep sensor stationary!");
    Serial.println("Calibration will take 5 seconds...");
    
    for (int i = 0; i < numSamples; i++) {
        float gx, gy, gz;
        float ax, ay, az;
        
        // Read raw data
        getGyroData(&gx, &gy, &gz);
        getAccelData(&ax, &ay, &az);
        
        // Accumulate sums
        gyroSumX += gx;
        gyroSumY += gy;
        gyroSumZ += gz;
        
        accelSumX += ax;
        accelSumY += ay;
        accelSumZ += az;
        
        // Progress indicator
        if (i % 100 == 0) {
            Serial.print(".");
        }
        
        delay(delayTime);
    }
    Serial.println();
    
    // Calculate averages (offsets)
    gyroOffsetX = gyroSumX / numSamples;
    gyroOffsetY = gyroSumY / numSamples;
    gyroOffsetZ = gyroSumZ / numSamples;
    
    // For accelerometer, we expect Z-axis to read +1g (16384 for ±2g range)
    // and X,Y axes to read 0 when level
    accelOffsetX = accelSumX / numSamples;
    accelOffsetY = accelSumY / numSamples;
    accelOffsetZ = (accelSumZ / numSamples) - 16384.0; // Adjust for gravity
    
    calibrated = true;
    
    Serial.println("Calibration Complete!");
    Serial.print("Gyro Offsets - X: "); Serial.print(gyroOffsetX);
    Serial.print(" Y: "); Serial.print(gyroOffsetY);
    Serial.print(" Z: "); Serial.println(gyroOffsetZ);
    
    Serial.print("Accel Offsets - X: "); Serial.print(accelOffsetX);
    Serial.print(" Y: "); Serial.print(accelOffsetY);
    Serial.print(" Z: "); Serial.println(accelOffsetZ);
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