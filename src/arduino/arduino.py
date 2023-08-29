# [pySerial API — pySerial 3.4 documentation](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.threaded.ReaderThread)

from settings import S, create_logger
log = create_logger(__file__, S.LOG_LEVEL)

import time
from datetime import datetime
import traceback
from typing import Optional, List
from pydantic import BaseModel
import serial
from serial.threaded import ReaderThread

SLOTS_SIZE = S.SLOTS_SIZE
SLEEP_SEC = 0.1

class Message(BaseModel):
    timestamp: str
    sender: str
    command: str
    sensors: List[Optional[int]] = list([None] * (SLOTS_SIZE+1))
    leds: List[Optional[List[int]]] = list([None] * (SLOTS_SIZE+1) * 2) # TODO 2 LEDs for each slot

class ArduinoControl():

    SLEEP_WAITING = 1
    TERMINATOR = b'\n'
    ENCODING = 'utf-8'
    UNICODE_HANDLING = 'replace'

    buffer = bytearray()
    _data_received = str()

    def read_raw_data(self) -> str:
        # TODO send signal from thread
        return self._data_received

    def clear_raw_data(self):
        self._data_received = None

    def connection_made(self, transport: ReaderThread):
        """Called when reader thread is started"""
        
        self.transport = transport

        while not self.transport.serial.in_waiting:
            time.sleep(self.SLEEP_WAITING)
            log.debug("Waiting port to be opened...")

        log.info(f'Port {self.transport.serial.port} is opened\n')

    def initialize(self):
        # Initialization
        self.transport.serial.flush()
        self.buffer = bytearray()
        while True:
            if self.read_raw_data() == "ARDUINO_IS_READY":
                log.info("SERVER_IS_READY")
                break
            else:
                log.debug("Waiting for 'ARDUINO_IS_READY'...")
                time.sleep(SLEEP_SEC)

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
        log.debug(f'<<< {self._data_received !r}')

    def write_line(self, text: str) -> None:
        self.transport.write(f"{text}\n".encode(self.ENCODING, self.UNICODE_HANDLING))
        
        log.debug(f">>> {text !r}")

    def connection_lost(self, exc: Exception) -> None:
        """Forget transport"""
        # TODO turn off leds
        log.info('Serial port is closed')
        try:
            self.transport = None
        except Exception :
            traceback.print_exception()


    def get_respond(self, command: str):  # TODO very ugly
        raw_respond = self.read_raw_data()

        # Ignore
        if (raw_respond is None
            or raw_respond == "ARDUINO_IS_READY"
            or raw_respond.startswith("[[ECHO]]")
            or raw_respond.startswith("[[DEBUG]]")):
            log.debug(f"Ignore {raw_respond = }")
            return None

        try:
            # TODO buggy
            respond: Message = Message.model_validate_json(raw_respond)
        except Exception as e:
            log.exception(e)
            return None
        respond.timestamp = datetime.now().isoformat()

        if respond.command != command:
            log.debug(f"Expected {command = }, but {respond.command = }")
            return None
        
        self.clear_raw_data()
        return respond
    
    def send_command(self, command, **kwarg):
        log.info(f"Send {command = }")
        msg = Message(command=command, sender="server", timestamp=datetime.now().isoformat(), **kwarg)
        self.write_line(msg.model_dump_json())

        while True:
            time.sleep(SLEEP_SEC)
            result = self.get_respond(command)
            if result:
                log.debug(f"{result = !r}")
                break

        return result


class ArduinoThread(ReaderThread):
    def __init__(self, port: str) -> None:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        super().__init__(ser, ArduinoControl)
    
    # type hint
    def __enter__(self) -> ArduinoControl:
        return super().__enter__()

if __name__ == '__main__':
    from settings import S
    log.debug("Arduino starts")

    # # TODO Add arduino stimulation
    # # TODO Add Arduino basic testing with json
    # with ArduinoThread(port=S.ARDUINO_PORT) as arduino:
    #     while True:
    #         log.debug("Hello world!")
    #         arduino.write_line(r"{}")
    #         time.sleep(1)
