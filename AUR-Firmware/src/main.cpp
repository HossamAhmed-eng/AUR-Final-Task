#include <Arduino.h>
#include <MPU6050.h>
#include <ESP32Encoder.h>
#include <kalman_filter.h>
#include <mqtt_comm.h>
#include <motordriver.h>
#include <gripper.h>


// Objects

MPU mpu;
Gripper arm(13, 180,80); //pin,open,close
Gripper gripper(12, 110 ,77);

ESP32Encoder leftEncoder;
ESP32Encoder rightEncoder;
const int leftEncoderA = 35;
const int leftEncoderB = 34;
const int rightEncoderA = 15;
const int rightEncoderB = 2;

float wheelbase = 28.4; // cm
float wheelradius = 3.25; // cm
int TICKS_PER_REV = 900;
KalmanFilter filter(wheelradius, wheelbase, TICKS_PER_REV);

    MotorDriver motors(23,5, 19, 22, 18, 21);//direction 2 = right

MQTTComm mqtt("ESPRobot", "123456789", "192.168.4.2");

long lastMsg = 0;
int last_left, last_right;
unsigned long last_time = 0;


// Callback

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
        //motors.setTargetRPM(150, 150);
        //motors.update();
    }
    else if (String(topic) == "robot/movement/down")
    {
        Serial.println("⬇️ Moving Backward");
        motors.moveBackward();
        //motors.update();
    }
    else if (String(topic) == "robot/movement/left")
    {
        Serial.println("⬅️ Turning Left");
        motors.turnLeft();
        //motors.update();
    }
    else if (String(topic) == "robot/movement/right")
    {
        Serial.println("➡️ Turning Right");
        motors.turnRight();
        //motors.update();
    }
    else if (String(topic) == "robot/stop")
    {
        Serial.println("🛑 Stop Moving");
        motors.stopMotors();
    }
    else if (String(topic) == "robot/gripper/open")
    {
        Serial.println("👐 Opening Gripper");
        gripper.open();
    }
    else if (String(topic) == "robot/gripper/close")
    {
        Serial.println("✊ Closing Gripper");
        gripper.close();
    }
    else if(String(topic)=="robot/gripper/up"){
        Serial.print("Box up");
        arm.close();
    }
    else if(String(topic)=="robot/gripper/down"){
        Serial.print("Box down");
        arm.open();
    }
}

// Tasks

//Task: Sensor & Kalman Filter 
void TaskSensors(void *pvParameters)
{
    for (;;)
    {
        //arm.close();
        //gripper.close();
        //gripper.close();
       float gx, gy, gz;
  mpu.getCalibratedGyroData(&gx, &gy, &gz);
    Serial.printf("Gyro: %.2f %.2f %.2f\n", gx, gy, gz);



        int current_left = leftEncoder.getCount(); // need to be in a different task
        int current_right = rightEncoder.getCount();
        Serial.print(current_left);
        Serial.println(current_right);
        float delta_left = current_left - last_left;
        float delta_right = current_right - last_right;
        float dt = (millis() - last_time) / 1000.0;

        filter.update(delta_left, delta_right, dt);

        last_left = current_left;
        last_right = current_right;
        last_time = millis();

        float x, y, heading;
        filter.getPosition(x, y, heading);
        Serial.printf("Position: X=%.2f Y=%.2f Heading=%.2f\n", x, y, heading);

        vTaskDelay(pdMS_TO_TICKS(100)); // 100 ms delay
    }
}

// Task: MQTT Loop & Publisher 
void TaskMQTT(void *pvParameters)
{
    for (;;)
    {
        mqtt.loop();

        long now = millis();
        if (now - lastMsg > 1000)
        {
            lastMsg = now;
            float x, y, heading;
            filter.getPosition(x, y, heading);
            

            char msg[64];
            sprintf(msg, "%.2f,%.2f", x, y);
            mqtt.publish("robot/coordinates", msg);
        }

        vTaskDelay(pdMS_TO_TICKS(100)); 
    }
}

// Setup

void setup()
{
    Serial.begin(115200);
    Serial.println("\n=== Robot Booting with FreeRTOS ===");

    // MPU
    mpu.init(0x68);
    mpu.configureGyro(250);
    mpu.configureAccel(2);

    // Motors
   // motors.begin(34, 35, 34, 35, 330.0);
    motors.begin();
    // Gripper
    arm.init();
    gripper.init();
    // Encoders
    leftEncoder.attachFullQuad(leftEncoderA, leftEncoderB);
    rightEncoder.attachFullQuad(rightEncoderA, rightEncoderB);
    leftEncoder.clearCount();
    rightEncoder.clearCount();

    // MQTT
    mqtt.begin();
    mqtt.setCallback(callback);

    //  Create FreeRTOS tasks 
    xTaskCreatePinnedToCore(TaskSensors, "TaskSensors", 4096, NULL, 2, NULL, 1);
    xTaskCreatePinnedToCore(TaskMQTT, "TaskMQTT", 4096, NULL, 1, NULL,0);
}

// app_main 
extern "C" void app_main(void)
{
    initArduino();
    setup();
    while (true)
    {
        vTaskDelay(1000);
    }
}
