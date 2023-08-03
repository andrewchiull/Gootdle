import time
import serial

class SerialControl():
    def __init__(self, port: str, baudrate=9600):
        self._data = None
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.ser.reset_input_buffer()
            self.running = False

        except serial.SerialException as e:
            print(e)
            return

        greeting =  "Connecting to Arduino..."
        print(greeting)

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

    def write(self, data: str):
        print(f"<<< {data}")
        self.ser.write(f"{data}\n".encode('utf-8'))

    def read(self):
        while self.ser.in_waiting():
            data = self.ser.readline().decode('utf-8').rstrip()
            print(f">>> {data}")

    def run(self):
        self.running = True
        while self.running:
            if self._data is not None:
                self.write(self._data)
                self._data = None
            self.read()


    def stop(self):
        self.running = False
        self.ser.close()
