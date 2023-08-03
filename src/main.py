import threading
import time

from settings import S

from src.arduino.arduino import ArduinoThread

def main():
    arduino = ArduinoThread(port=S.ARDUINO_PATH)
    thread_arduino = threading.Thread(target=arduino.update)
    thread_arduino.start()

    try:
        arduino._write = "Start"
        while True:
            time.sleep(0.1)
            print(">>> Command: ", end="")
            
            arduino._write = input()
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    main()