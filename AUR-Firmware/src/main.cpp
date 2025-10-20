// main.cpp
#include <Arduino.h>
#include <MPU6050.h>
#include <ESP32Encoder.h>
#include <kalman_filter.h>
#include <mqtt_comm.h>
MPU mpu; // init

//----------Encoders----------
ESP32Encoder leftEncoder;
ESP32Encoder rightEncoder;
const int leftEncoderA = 35;
const int leftEncoderB = 33;
const int rightEncoderA = 27;
const int rightEncoderB = 12;
float wheelbase = 0;
float wheelradius = 0;
int TICKS_PER_REV = 0;
KalmanFilter filter(wheelradius, wheelbase, TICKS_PER_REV);
//----------------------------
//----------WiFi and MQTT Settings----------
MQTTComm mqtt("REPLACE_WITH_SSID", "REPLACE_WITH_PASSWORD", "MQTT_BROKER_IP_ADDRESS");
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
    Serial.println("======================================");
    Serial.print("Message arrived on topic: ");
    Serial.println(topic);
    String messageTemp;
    for (int i = 0; i < length; i++)
    {
        messageTemp += (char)message[i];
    }
    Serial.println(messageTemp);
    Serial.println("======================================");
    // example to test stuff
    if (String(topic) == "esp32/output")
    {
        if (messageTemp == "on")
        {
            // digitalWrite(ledPin, HIGH);
            Serial.println("LED turned ON");
        }
        else if (messageTemp == "off")
        {
            // digitalWrite(ledPin, LOW);
            Serial.println("LED turned OFF");
        }
    }
}
void setup()
{
    Serial.begin(115200);
    mpu.init(0x68);         // MPU6050 default I2C address
    mpu.configureGyro(250); // ±250 dps
    mpu.configureAccel(2);  // ±2g
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
    Serial.print("Position: X=");
    Serial.print(x);
    Serial.print(" Y=");
    Serial.print(y);
    Serial.print(" Heading=");
    Serial.println(heading);
    //-----------------------------
    // MQTT stuff
    mqtt.loop();

    long now = millis();
    if (now - lastMsg > 5000)
    {
        lastMsg = now;

        float gx, gy, gz;
        float ax, ay, az;
        mpu.getGyroData(&gx, &gy, &gz);
        mpu.getAccelData(&ax, &ay, &az);

        char msg[32];
        sprintf(msg, "%0.2f", gx);
        mqtt.publish("esp32/gx", msg);
        sprintf(msg, "%0.2f", gy);
        mqtt.publish("esp32/gy", msg);
        sprintf(msg, "%0.2f", gz);
        mqtt.publish("esp32/gz", msg);
    }
    //-----------------------------
    delay(100);
}