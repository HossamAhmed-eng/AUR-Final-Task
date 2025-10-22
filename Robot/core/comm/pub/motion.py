from sshkeyboard import listen_keyboard
class PressHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.current_movement = None 

    def press(self, key):
        print(f"Key pressed: {key}")
        try:
            if key in ["up", "down", "left", "right"]:
                if self.current_movement != key:
                    self.mqtt_client.publish(f"robot/movement/{key}", "start moving")
                    print(f" Published to robot/movement/{key}")
                    self.current_movement = key
                else:
                    print(f"Continuing: {key}")
                    
            elif key == "space":
                self.mqtt_client.publish("robot/stop", "stop moving")
                print("Published to robot/stop")
                self.current_movement = None
                
            elif key == "o":
                self.mqtt_client.publish("robot/gripper/open", "open gripper")
                print("Published to robot/gripper/open")
                
            elif key == "c":
                self.mqtt_client.publish("robot/gripper/close", "close gripper")
                print("Published to robot/gripper/close")
            else:
                print(f"Unmapped key: {key}")

        except Exception as e:
            print(f"Error publishing: {e}")

    def release(self, key):
        pass

    def start_listening(self):
        listen_keyboard(on_press=self.press, on_release=self.release)
