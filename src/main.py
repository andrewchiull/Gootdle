import time
from time import sleep
from datetime import datetime
from typing import List
from pydantic import BaseModel

from settings import S

from src.arduino.arduino import ArduinoThread, ArduinoControl

class Message(BaseModel):
    timestamp: str
    sender: str
    command: str
    sensors: List[int] = list()
    leds: List[int] = list()


THRESHOLD = 0.2
SLEEP_SEC = 0.5
DEBUG = True
DEBUG = False

def weight(sensor: int) -> float:
    return sensor/1024

def main():
    with ArduinoThread(port=S.ARDUINO_PATH) as arduino:
        arduino: ArduinoControl # NOT a ArduinoThread object!!!
        arduino.debug = DEBUG

        def get_respond():
            respond: Message = Message.model_validate_json(arduino.read())
            respond.timestamp = datetime.now().isoformat()
            return respond
        
        def command(command, **kwarg):
            msg = Message(command=command, sender="server", timestamp=datetime.now().isoformat(), **kwarg)
            print(f"{msg!r}")
            arduino.write_line(msg.model_dump_json())

        arduino.write_line("Hello world")
        while True:
            command("read_sensors")
            
            sleep(SLEEP_SEC)

            read_sensors_respond = get_respond()
            print(f"{read_sensors_respond!r}")
            print()
            
            sleep(SLEEP_SEC)
            
            
            
            
            leds = list()
            for sensor in read_sensors_respond.sensors:
                leds.append(int(weight(sensor) > THRESHOLD))
            
            command("write_leds", leds=leds)
            
            sleep(SLEEP_SEC)

            write_leds_respond = get_respond()
            print(f"{write_leds_respond!r}")
            print()
            sleep(SLEEP_SEC)
            
            



if __name__ == "__main__":
    main()