import serial
import threading
import time

from settings import S

class ArduinoReader(threading.Thread):
    def __init__(self, port, baudrate=9600):
        try:
            threading.Thread.__init__(self)
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.serial.reset_input_buffer()
            self.running = False

        except serial.SerialException as e:
            self.print(e)
            return

    def run(self):
        self.running = True
        while self.running:
            if self.serial.inWaiting():
                data = self.serial.readline().decode().strip()
                print("Received: ", data)
            time.sleep(0.01)  # short sleep to prevent busy-waiting

    def stop(self):
        self.running = False
        self.serial.close()


if __name__ == "__main__":
    arduino = ArduinoReader(port=S.ARDUINO_PORT, baudrate=9600)  # replace with your port and baudrate
    arduino.start()

    try:
        while True:
            time.sleep(1)  # main thread does other stuff
    except KeyboardInterrupt:
        print("Stopping...")
        arduino.stop()
