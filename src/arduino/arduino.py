# [pySerial API — pySerial 3.4 documentation](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.threaded.ReaderThread)

import sys
import time
import traceback
import serial
from serial.threaded import LineReader, ReaderThread

from settings import S

class PrintLines(LineReader):
    
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write(f'Port {transport.serial.port} is opened\n')
        self.write_line('hello world')

    def handle_line(self, data: str):
        data = data.rstrip() # Remove '\r'
        sys.stdout.write('>>> {}\n'.format(repr(data)))

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('Serial port is closed\n')

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
