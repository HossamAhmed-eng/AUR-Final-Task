// main.cpp
#include <Arduino.h>
#include <MPU6050.h>
#include <ESP32Encoder.h>
#include <kalman_filter.h>
#include <mqtt_comm.h>
#include <motor.h>
#include <gripper.h>
MPU mpu; // init
// Motors
//left motor = direction1
//right motor = direction2
Gripper gripper(12, 0, 90); // pin, openAngle, closeAngle
Motor leftMotor(21, 22, 19, 0, 5000, 8);   // pwmPin, dir1, dir2, channel, freq, resolution
Motor rightMotor(19, 23, 5, 1, 5000, 8);
//
//----------Encoders----------
ESP32Encoder leftEncoder;
ESP32Encoder rightEncoder;
const int leftEncoderA = 34;
const int leftEncoderB = 35;
const int rightEncoderA = 2;
const int rightEncoderB = 15;
float wheelbase = 0;
float wheelradius = 0;
int TICKS_PER_REV = 0;
KalmanFilter filter(wheelradius, wheelbase, TICKS_PER_REV);
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
void moveForward() {
    leftMotor.setSpeed(80);
    rightMotor.setSpeed(80);
}

void moveBackward() {
    leftMotor.setSpeed(-80);
    rightMotor.setSpeed(-80);
}

void turnLeft() {
    leftMotor.setSpeed(-70);
    rightMotor.setSpeed(70);
}

void turnRight() {
    leftMotor.setSpeed(70);
    rightMotor.setSpeed(-70);
}

void stopMotors() {
    leftMotor.stop();
    rightMotor.stop();
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
        moveForward();
    }
    else if (String(topic) == "robot/movement/down")
    {
        Serial.println("⬇️ Moving Backward");
        moveBackward();
    }
    else if (String(topic) == "robot/movement/left")
    {
        Serial.println("⬅️ Turning Left");
        turnLeft();
    }
    else if (String(topic) == "robot/movement/right")
    {
        Serial.println("➡️ Turning Right");
        turnRight();
    }
    else if (String(topic) == "robot/stop")
    {
        Serial.println("🛑 Stop Moving");
        stopMotors();
    }
    else if (String(topic) == "robot/gripper/open")
    {
        Serial.println("👐 Opening Gripper");
        // gripperOpen();
    }
    else if (String(topic) == "robot/gripper/close")
    {
        Serial.println("✊ Closing Gripper");
        // gripperClose();
    }
}

void setup()
{
    Serial.begin(115200);
    mpu.init(0x68);         // MPU6050 default I2C address
    mpu.configureGyro(250); // ±250 dps
    mpu.configureAccel(2);  // ±2g
    // Motor initialization
    leftMotor.init();
    rightMotor.init();
    // Kalman Filter Initialization
    filter.begin();
    filter.setPosition(0, 0, 0);
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
    // Kalman Filter stuff ---------
    float left_ticks = leftEncoder.getCount();
    float right_ticks = rightEncoder.getCount();
    // float leftRevs = (float)left_ticks / TICKS_PER_REV;
    // float rightRevs = (float)right_ticks / TICKS_PER_REV;
    float dt = 0.1;
    filter.update(left_ticks, right_ticks, dt);
    float x, y, heading;
    filter.getPosition(x, y, heading);
   /* Serial.print("Position: X=");
    Serial.print(x);
    Serial.print(" Y=");
    Serial.print(y);
    Serial.print(" Heading=");
    Serial.println(heading);*/
    //-----------------------------
    // MQTT stuff
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