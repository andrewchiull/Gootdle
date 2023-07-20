from PyQt5.QtCore import QObject
import time
import serial


class SerialControl(QObject):
    command = None

    def setupSerial(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0.1)
        except serial.SerialException as e:
            self.print(e)
            try:
                self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
            except serial.SerialException as e:
                self.print(e)
                try:
                    self.ser = serial.Serial('/dev/tty.usbmodem1411201', 9600, timeout=0.1)
                except serial.SerialException as e:
                    self.print(e)
                    return
                return
            return

        self.ser.reset_input_buffer()

        greeting =  "Connecting to Arduino..."
        self.print(greeting)
        self.ser.write(f"{greeting}\n".encode('utf-8'))

        count_try = 0
        while True:
            count_try += 1
            self.ser.write(f"{greeting}\n".encode('utf-8'))
            self.print(f"Waiting for respond... [{count_try}]")
            try:
                respond = self.ser.readline().decode('utf-8').rstrip()
            except UnicodeDecodeError:
                pass

            self.print(f"Respond: {respond}")
            if greeting in respond:
                self.print("Successfully connected to Arduino!\n")
                break
            time.sleep(1/5)

    def writeSerial(self, command: str):
        self.print(f"<<< {command}")
        self.ser.write(f"{command}\n".encode('utf-8'))
        self.readSerial()

    def readSerial(self):
        # Read echo
        while True:
            line = self.ser.readline().decode('utf-8').rstrip()
            if line == "":
                break
            self.print(f">>> {line}")

    def print(self, text: str = ""):
        print(text)

    def run(self):
        self.setupSerial()
        while True:
            if self.command is not None:
                self.writeSerial(self.command)
                self.command = None
            self.readSerial()

