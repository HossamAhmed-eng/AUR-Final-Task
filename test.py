from paho.mqtt.client import Client as MC
from paho.mqtt.enums import CallbackAPIVersion
from time import sleep
from random import random


_mqttc = MC(CallbackAPIVersion.VERSION2)

def _on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(" Failed to connect. Retrying...")
    else:
        print(" Connected to MQTT broker.")
        client.subscribe("robot/movement/#")
        print(" Subscribed to: robot/movement/#")


def _on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f" Movement message received → Topic: {topic}, Payload: {payload}")

def setup(address="localhost", port=1883):
    _mqttc.on_connect = _on_connect
    _mqttc.on_message = _on_message
    _mqttc.connect(address, port)
    _mqttc.loop_start()  

if __name__ == "__main__":
    setup()

    while True:
        sleep(1)
        x = random()
        y = random()
        _mqttc.publish("robot/coordinates", f"{x},{y}")
        print(f" Published coordinates: X={x:.2f}, Y={y:.2f}")
