# keyboard_test_only.py
from sshkeyboard import listen_keyboard
import time

def press(key):
    print(f"Key '{key}' pressed")
    
    if key in ["up", "down", "left", "right"]:
        print(f"🚗 ROBOT ACTION: Start moving {key.upper()}")
        print(f"   (This would publish: robot/movement/{key})")
        
    elif key == "space":
        print("🛑 ROBOT ACTION: Stop all movement")
        print("   (This would publish: robot/stop)")
        
    elif key.lower() == "o":
        print("🖐️ ROBOT ACTION: Open gripper")
        print("   (This would publish: robot/gripper/open)")
        
    elif key.lower() == "c":
        print("✊ ROBOT ACTION: Close gripper")
        print("   (This would publish: robot/gripper/close)")
        
    else:
        print(f"❌ Unmapped key: {key}")

def release(key):
    print(f"Key '{key}' released - Robot continues moving")
    # No stop command sent!

print("🎮 Keyboard Controller Test (No MQTT)")
print("=====================================")
print("Controls:")
print("  ↑ ↓ ← → : Movement (continues after release)")
print("  SPACE   : Stop all movement")
print("  O       : Open gripper")
print("  C       : Close gripper")
print("  ESC     : Exit")
print("=====================================")

listen_keyboard(
    on_press=press,
    on_release=release,
    until="esc"
)