#include "mqtt_comm.h"
#include <Arduino.h>

MQTTComm::MQTTComm(const char *ssid,
                   const char *password,
                   const char *mqtt_server)
    : wifi_ssid(ssid),
      wifi_pass(password),
      mqtt_server_addr(mqtt_server),
      client(espClient)
{
}

void MQTTComm::begin()
{
    setupWiFi();
    client.setServer(mqtt_server_addr, 1883);
}

void MQTTComm::loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();
}

void MQTTComm::setCallback(MQTT_CALLBACK_SIGNATURE)
{
    client.setCallback(callback);
}

void MQTTComm::publish(const char *topic, const char *payload)
{
    client.publish(topic, payload);
}

void MQTTComm::setupWiFi()
{
    WiFi.softAP(wifi_ssid, wifi_pass);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);
}

void MQTTComm::reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP32Client"))
        {
            Serial.println("connected");
           // client.subscribe("esp32/#");
            client.subscribe("robot/movement/up");
            client.subscribe("robot/movement/down");
            client.subscribe("robot/movement/left");
            client.subscribe("robot/movement/right");
            client.subscribe("robot/stop");
            client.subscribe("robot/gripper/open");
            client.subscribe("robot/gripper/up");
            client.subscribe("robot/gripper/down");
            client.subscribe("robot/gripper/close");
            Serial.println("Subscribed to topic: robot/movement/");
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" -> retrying in 5 seconds");
            delay(5000);
        }
    }
}
