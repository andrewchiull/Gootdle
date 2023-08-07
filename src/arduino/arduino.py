# [pySerial API — pySerial 3.4 documentation](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.threaded.ReaderThread)

import time
import traceback
import serial
from serial.threaded import ReaderThread

from settings import S
SLEEP_TIME = 1

class ArduinoControl():
    
    debug = True

    TERMINATOR = b'\n'
    ENCODING = 'utf-8'
    UNICODE_HANDLING = 'replace'

    buffer = bytearray()
    _data_received = str()

    def read(self) -> str:
        return self._data_received

    def connection_made(self, transport):
        """Called when reader thread is started"""
        
        self.transport = transport

        while not self.transport.serial.in_waiting:
            time.sleep(SLEEP_TIME)
            self.print("Waiting port to be opened...")

        self.print(f'Port {self.transport.serial.port} is opened\n')

    def print(self, message: str):
        # TODO add logging
        # TODO add color # import colorama
        if self.debug:
            print(f"[INFO] {message}")

    def data_received(self, data):
        """Buffer received data, find TERMINATOR, call handle_packet"""
        self.buffer.extend(data)
        while self.TERMINATOR in self.buffer:
            packet, self.buffer = self.buffer.split(self.TERMINATOR, 1)
            self.handle_packet(packet)

    def handle_packet(self, packet: bytearray) -> str:
        self.handle_line(packet.decode(self.ENCODING, self.UNICODE_HANDLING))

    def handle_line(self, data: str):
        self._data_received = data.rstrip() # Remove '\r' or '\n'
        self.print(f'<<< {self._data_received !r}')

    def write_line(self, text: str) -> None:
        self.transport.write(f"{text}\n".encode(self.ENCODING, self.UNICODE_HANDLING))
        
        self.print(f">>> {text !r}")

    def connection_lost(self, exc: Exception) -> None:
        """Forget transport"""
        self.print('Serial port is closed')
        try:
            self.transport = None
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
