import sys
import time
import traceback
import serial
from serial.threaded import LineReader, ReaderThread

from settings import S

class PrintLines(LineReader):
    
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write('port opened\n')
        self.write_line('hello world')

    def handle_line(self, data: str):
        data = data.rstrip() # Remove '\r'
        sys.stdout.write('line received: {}\n'.format(repr(data)))

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('port closed\n')
    


ser = serial.Serial(S.ARDUINO_PORT, baudrate=9600, timeout=1)
with ReaderThread(ser, PrintLines) as protocol:
    while True:
        protocol.write_line('hello')
        time.sleep(1)