# [pySerial API — pySerial 3.4 documentation](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.threaded.ReaderThread)

import sys
import time
import traceback
import serial
from serial.threaded import LineReader, ReaderThread

from settings import S

class ArduinoControl(LineReader):
    
    debug = True
    _data_received = str()

    def read(self) -> str:
        return self._data_received
    
    def connection_made(self, transport):
        super(ArduinoControl, self).connection_made(transport)
        while not self.transport.serial.in_waiting:
            time.sleep(1)
            self.print("Waiting port to be opened...")

        self.print(f'Port {self.transport.serial.port} is opened\n')

    def print(self, message: str):
        if self.debug:
            print(f">>> {message}")

    def write_line(self, text: str) -> None:
        self.print(f"[Sent] {text}")
        return super().write_line(text)

    def handle_line(self, data: str):
        self._data_received = data.rstrip() # Remove '\r' or '\n'
        self.print(f'[Received] {self._data_received!r}')

    def connection_lost(self, exc: Exception) -> None:
        self.print('Serial port is closed')

        try:
            super().connection_lost(exc)
        except Exception:
            traceback.print_exception()

class ArduinoThread(ReaderThread):
    def __init__(self, port: str) -> None:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        super().__init__(ser, ArduinoControl)
    
    # type hint
    def __enter__(self) -> ArduinoControl:
        return super().__enter__()

if __name__ == '__main__':
    with ArduinoThread(S.ARDUINO_PATH) as arduino:
        arduino: ArduinoControl
        while True:
            arduino.write_line("hello")
            time.sleep(1)
