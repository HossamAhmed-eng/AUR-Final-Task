import threading
from paho.mqtt.client import Client as MC
from paho.mqtt.enums import CallbackAPIVersion
import Robot.core.comm.sub.coords as coords
from Robot.core.comm.pub.motion import PressHandler

_mqttc = MC(CallbackAPIVersion.VERSION2)

# --------MQTT Configuration--------
#           ---topics---
# coordinates topic: 'robot/coordinates'
# movement topic: 'robot/movement/<direction>' where <direction> is 'up', 'down', 'left', 'right'
# stop topic: 'robot/stop'
# open gripper topic: 'robot/gripper/open'
# close gripper topic: 'robot/gripper/close'
# --------broker: '192.168.4.2'--------
#-----------port: 1883----------

def _on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print("Failed to connect. Retrying...")
    else:
        client.subscribe("robot/coordinates")
        client.message_callback_add("robot/coordinates", coords.callback)
        print("Connected to MQTT broker and subscribed to: robot/coordinates")

def setup(coords_slot, address="192.168.4.2", port=1883):
    coords.slot = coords_slot
    _mqttc.on_connect = _on_connect
    _mqttc.connect(address, port)
    _mqttc.loop_start()
    thread = threading.Thread(target=publish, daemon=True)
    thread.start()

def publish():
    handler = PressHandler(_mqttc)
    handler.start_listening()

def stop():
    _mqttc.loop_stop()
    _mqttc.disconnect()