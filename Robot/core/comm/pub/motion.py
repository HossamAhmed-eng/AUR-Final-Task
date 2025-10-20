from sshkeyboard import listen_keyboard
from paho.mqtt.client import Client as MC
from paho.mqtt.enums import CallbackAPIVersion

client = MC(CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(" Failed to connect to MQTT broker.")
    else:
        print(" Connected to MQTT broker.")
        

client.on_connect = on_connect
client.connect("192.168.4.2", 1883)
client.loop_start()

def press(key):
    print(f" Key pressed: {key}")
    if key in ["up", "down", "left", "right"]:
        client.publish(f"robot/movement/{key}", "start moving")
        print(f" Published to robot/movement/{key}")
    elif key == "space":
        client.publish("robot/stop", "stop moving")
        print(" Published to robot/stop")
    elif key == "o":
        client.publish("robot/gripper/open", "open gripper")
        print(" Published to robot/gripper/open")
    elif key == "c":
        client.publish("robot/gripper/close", "close gripper")
        print("  Published to robot/gripper/close")

def release(key):
    pass

listen_keyboard(on_press=press, on_release=release)
