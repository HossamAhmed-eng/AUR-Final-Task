// main.cpp
#include <Arduino.h>
#include <MPU6050.h>
#include <ESP32Encoder.h>
#include <kalman_filter.h>
#include <mqtt_comm.h>
#include <motortest.h>
#include <gripper.h>
MPU mpu; // init
// Motors
//left motor = direction1
//right motor = direction2
Gripper gripper(12, 0, 90); // pin, openAngle, closeAngle

//
//----------Encoders----------
ESP32Encoder leftEncoder;
ESP32Encoder rightEncoder;
const int leftEncoderA = 34;
const int leftEncoderB = 35;
const int rightEncoderA = 2;
const int rightEncoderB = 15;
float wheelbase = 28.4; // in cm
float wheelradius = 32.5; // in mm
int TICKS_PER_REV = 900;
KalmanFilter filter(wheelradius, wheelbase, TICKS_PER_REV);
MotorDriver motors(22, 18, 19, 23, 5, 21); // in1,  in2,  ena,  in3,  in4,  enb
//----------------------------
//----------WiFi and MQTT Settings----------
MQTTComm mqtt("ESPRobot", "123456789", "192.168.4.2");
long lastMsg = 0;

//-----------------------------------------
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

void callback(char *topic, byte *message, unsigned int length)
{
    String msg;
    for (unsigned int i = 0; i < length; i++)
        msg += (char)message[i];

    Serial.print("Topic: ");
    Serial.println(topic);
    Serial.print("Message: ");
    Serial.println(msg);

     if (String(topic) == "robot/movement/up")
     {
         Serial.println("⬆️ Moving Forward");
         motors.moveForward();
         motors.setTargetRPM(150, 150);
         motors.update();
     }
     else if (String(topic) == "robot/movement/down")
     {
         Serial.println("⬇️ Moving Backward");
         motors.moveBackward();
         motors.update();
     }
     else if (String(topic) == "robot/movement/left")
     {
         Serial.println("⬅️ Turning Left");
         motors.turnLeft();
         motors.update();
     }
     else if (String(topic) == "robot/movement/right")
     {
         Serial.println("➡️ Turning Right");
         motors.turnRight();
         motors.update();
     }
     else if (String(topic) == "robot/stop")
     {
         Serial.println("🛑 Stop Moving");
         motors.stopMotors();
         //motors.update();
     }
     else if (String(topic) == "robot/gripper/open")
     {
         Serial.println("👐 Opening Gripper");
         // gripperOpen();
         gripper.open();
     }
     else if (String(topic) == "robot/gripper/close")
     {
         Serial.println("✊ Closing Gripper");
         // gripperClose();
         gripper.close();
     }
}
const int IN3 = 22;
const int IN4 = 19;
const int ENB = 21;
const int freq = 1000;    // PWM frequency (Hz)
const int pwmChannel = 0; // choose 0–15 (ESP32 supports 16 channels)
const int resolution = 8;
int last_left,last_right;
unsigned long last_time=0;
void setup()
{
    Serial.begin(115200);
    mpu.init(0x68);         // MPU6050 default I2C address
    mpu.configureGyro(250); // ±250 dps
    mpu.configureAccel(2);  // ±2g
    // Motor initialization
    //motors.begin();
    motors.begin(34, 35, 34, 35, 330.0); // leftEncA, leftEncB, rightEncA, rightEncB, ticksPerRev
    // Kalman Filter Initialization
    //filter.begin();
    //filter.setPosition(0, 0, 0);
    gripper.init();
    // Encoder Initialization
    leftEncoder.attachFullQuad(leftEncoderA, leftEncoderB);
    rightEncoder.attachFullQuad(rightEncoderA, rightEncoderB);
    leftEncoder.clearCount();
    rightEncoder.clearCount();
    // WiFi and MQTT Initialization
    mqtt.begin();
    mqtt.setCallback(callback);
    
}

void loop()
{
     float gx, gy, gz;
  mpu.getGyroData(&gx, &gy, &gz);
    Serial.printf("Gyro: %.2f %.2f %.2f\n", gx, gy, gz);

    // Kalman Filter stuff ---------
    float left_ticks = leftEncoder.getCount();
    float right_ticks = rightEncoder.getCount();
    Serial.print("Left Encoder Ticks: ");
    Serial.print(left_ticks);
    Serial.print(" | Right Encoder Ticks: ");
    Serial.println(right_ticks);
    /* motors.setTargetRPM(150, 150); // move forward
     motors.update();

     // Example stop after 5s
     if (millis() > 5000)
         motors.stop();
*/

    // float leftRevs = (float)left_ticks / TICKS_PER_REV;
    // float rightRevs = (float)right_ticks / TICKS_PER_REV;
    int current_left = leftEncoder.getCount();
    int current_right = rightEncoder.getCount();

    float delta_left = current_left - last_left;
    float delta_right = current_right - last_right;

    float dt = (millis() - last_time) / 1000.0; // seconds

filter.update(delta_left, delta_right, dt);

last_left = current_left;
last_right = current_right;
last_time = millis();
float x, y, heading;
filter.getPosition(x, y, heading);
    Serial.print("Position: X=");
    Serial.print(x);
    Serial.print(" Y=");
    Serial.print(y);
    Serial.print(" Heading=");
    Serial.println(heading);
/*
    float dt = 0.1;
    filter.update(left_ticks, left_ticks, dt);
    float x, y, heading;
    filter.getPosition(x, y, heading);
    Serial.print("Position: X=");
    Serial.print(x);
    Serial.print(" Y=");
    Serial.print(y);
    Serial.print(" Heading=");
    Serial.println(heading);
    //-----------------------------
    // MQTT stuff
  */  
    mqtt.loop();

    long now = millis();
    if (now - lastMsg > 1000) // every second
    {
        lastMsg = now;
        char msg[64];
        float xx=random(0,100)/10.0;
        float yy=random(0,100)/10.0;
        sprintf(msg, "%.2f,%.2f", xx, yy);

    // Publish to MQTT
    mqtt.publish("robot/coordinates", msg);
    }
    //-----------------------------
    delay(100);
}