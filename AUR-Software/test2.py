# simple_test.py
from paho.mqtt.client import Client as MC
from paho.mqtt.enums import CallbackAPIVersion
from Robot.core.comm.pub.motion import PressHandler
import time

_mqttc = MC(CallbackAPIVersion.VERSION2)

def setup():
    try:
        _mqttc.connect("localhost", 1883, 60)
        _mqttc.loop_start()
        time.sleep(2)
        return True
    except:
        return False

if setup():
    handler = PressHandler(_mqttc)
    handler.start_listening()
else:
    print("❌ Could not connect to MQTT broker")