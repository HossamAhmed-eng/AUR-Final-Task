#ifndef MQTT_COMM_H
#define MQTT_COMM_H

#include <WiFi.h>
#include <PubSubClient.h>

class MQTTComm
{
public:
    MQTTComm(const char *ssid,
             const char *password,
             const char *mqtt_server);

    void begin();
    void loop();
    void setCallback(MQTT_CALLBACK_SIGNATURE);
    void publish(const char *topic, const char *payload);

private:
    const char *wifi_ssid;
    const char *wifi_pass;
    const char *mqtt_server_addr;

    WiFiClient espClient;
    PubSubClient client;

    void setupWiFi();
    void reconnect();
};

#endif
