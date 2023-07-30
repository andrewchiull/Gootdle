import threading
import time


from src.cv import camera
from src.serial import serialControl

cam = camera.Camera()
ser = serialControl.SerialControl()



def main():
    serial_controller = ser
    thread = threading.Thread(target=serial_controller.run)
    thread.start()

    try:
        serial_controller.command = "Start"
        while True:
            time.sleep(0.1)
            print(">>> Command: ", end="")
            
            serial_controller.command = input()
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    main()