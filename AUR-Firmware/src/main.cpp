// main.cpp
#include <Arduino.h>
#include <MPU6050.h>
MPU mpu; //init
// #include "kalman_filter.h"

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
float x,y,theta; 
float wheelbase=0; //placeholder
float wheelradius=0; //placeholder
int TICKS_PER_REV=0; //placeholder
// KalmanFilter filter(wheelradius, wheelbase, TICKS_PER_REV);
volatile long leftTicks=0, rightTicks=0;
void encoderTask(void *pvParameters)
{
    static long prevLeftTicks = 0;
    static long prevRightTicks = 0;
    while(true){
        long L=leftTicks;
        long R=rightTicks;
        long dL = L - prevLeftTicks;
        long dR = R - prevRightTicks;
        prevLeftTicks=L;
        prevRightTicks=R;
        float dSL=(dL*2*3.14159*wheelradius)/TICKS_PER_REV;
        float dSR=(dR*2*3.14159*wheelradius)/TICKS_PER_REV;
        float dS=(dSL+dSR)/2.0;
        float dTheta=(dSR - dSL)/wheelbase;
    }
}

void setup()
{
    Serial.begin(115200);
    mpu.init(0x68);         // MPU6050 default I2C address
    mpu.configureGyro(250); // ±250 dps
    mpu.configureAccel(2);  // ±2g
    /*xTaskCreate(
        encoderTask,   
        "EncoderTask", 
        2048,          
        NULL,          
        1,             
        NULL           
    );*/

    /*
    filter.begin();
    filter.setPosition(0, 0, 0);
    */
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
    /*
    float left_ticks = readLeftEncoder();
    float right_ticks = readRightEncoder();
    float dt = 0.1;

    filter.update(left_ticks, right_ticks, dt);

    float x, y, heading;
    filter.getPosition(x, y, heading);

    Serial.print("Position: X=");
    Serial.print(x);
    Serial.print(" Y=");
    Serial.print(y);
    Serial.print(" Heading=");
    Serial.println(heading);
    */

    delay(100);
}
