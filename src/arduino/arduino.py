# [pySerial API — pySerial 3.4 documentation](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.threaded.ReaderThread)

import sys
import threading
import time
import traceback
import serial
from serial.threaded import LineReader, ReaderThread
import json

from settings import S

class PrintLines(LineReader):
    
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        while not self.transport.serial.in_waiting:
            time.sleep(1)
            sys.stdout.write("Waiting...\n")

        sys.stdout.write(f'Port {transport.serial.port} is opened\n')

    def write_line(self, text: str) -> None:
        sys.stdout.write(f"Sent: {text}\n")
        return super().write_line(text)

    def handle_line(self, data: str):
        data = data.rstrip() # Remove '\r' or '\n'
        sys.stdout.write(f'>>> {data!r}\n')

    def connection_lost(self, exc: Exception) -> None:
        sys.stdout.write('Serial port is closed\n')

        try:
            super().connection_lost(exc)
        except Exception:
            traceback.print_exception()

    def write_json(self, data: dict) -> None:
        text = json.dumps(data)
        return super().write_line(text)

class ArduinoThread(ReaderThread):
    def __init__(self, port: str) -> None:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        super().__init__(ser, PrintLines)
    
    # type hint
    def __enter__(self) -> PrintLines:
        return super().__enter__()

if __name__ == '__main__':
    with ArduinoThread(S.ARDUINO_PATH) as arduino:
        while True:
            arduino.write_line("hello")
            time.sleep(1)
