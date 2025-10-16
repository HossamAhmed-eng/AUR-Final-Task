// main.cpp
#include <Arduino.h>
#include <MPU6050.h>

MPU mpu; //init


void setup();
void loop();

extern "C" void app_main(void)
{
    initArduino();
    setup();
    while (true)
    {
        loop();
        vTaskDelay(1);
    }
}
void setup()
{
    Serial.begin(115200);
    mpu.init(0x68);         // MPU6050 default I2C address
    mpu.configureGyro(250); // ±250 dps
    mpu.configureAccel(2);  // ±2g
}

void loop()
{
    //THIS is only a test so far for the driver not final.
    float gx, gy, gz, ax, ay, az;

    mpu.getGyroData(&gx, &gy, &gz);
    mpu.getAccelData(&ax, &ay, &az);
    float ax_g = ax / 16384.0;
    float ay_g = ay / 16384.0;
    float az_g = az / 16384.0;
    float gx_dps = gx / 131;
    float gy_dps = gy / 131;
    float gz_dps = gz / 131;
    float pitch = mpu.getPitch(ax_g, ay_g, az_g);
    float roll  = mpu.getRoll(ax_g, ay_g, az_g); 
    Serial.println("=== Sensor Readings ===");
    Serial.printf("Accel [g]: X=%.3f, Y=%.3f, Z=%.3f\n", ax_g, ay_g, az_g);
    Serial.printf("Gyro  [°/s]: X=%.2f, Y=%.2f, Z=%.2f\n", gx_dps, gy_dps, gz_dps);
    Serial.printf("Pitch: %.2f deg, Roll: %.2f deg\n", pitch, roll);
    Serial.println("----------------------");

    delay(100);
}
