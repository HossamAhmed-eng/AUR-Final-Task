from sshkeyboard import listen_keyboard

class PressHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.current_movement = None

    def press(self, key):
        try:
            if key in ["up", "down", "left", "right"]:
                if self.current_movement != key:
                    self.mqtt_client.publish(f"robot/movement/{key}", "start moving")
                    print(f" Moving {key}")
                    self.current_movement = key

            elif key == "space":
                self.mqtt_client.publish("robot/stop", "stop moving")
                print(" Emergency stop")
                self.current_movement = None

            elif key == "o":
                self.mqtt_client.publish("robot/gripper/open", "open gripper")
                print("Gripper opened")

            elif key == "c":
                self.mqtt_client.publish("robot/gripper/close", "close gripper")
                print("Gripper closed")
            elif key == "u":
                self.mqtt_client.publish("robot/gripper/up","gripper up")
                print("Gripper up")
            elif key =="d":
                self.mqtt_client.publish("robot/gripper/down","gripper down")
                print("Gripper down")

            else:
                print(f"Unmapped key: {key}")

        except Exception as e:
            print(f"Error publishing on press: {e}")

    def release(self, key):
        try:
            if key in ["up", "down", "left", "right"]:
                self.mqtt_client.publish(f"robot/stop", "stop moving")
                print(f" Stopped moving {key}")
                if self.current_movement == key:
                    self.current_movement = None
        except Exception as e:
            print(f"Error publishing on release: {e}")

    def start_listening(self):
        print(" Listening for keyboard input... ")
        listen_keyboard(on_press=self.press, on_release=self.release)
