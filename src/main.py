import time
from datetime import datetime
from typing import List
from pydantic import BaseModel

from settings import S

from src.arduino.arduino import ArduinoThread

class Message(BaseModel):
    timestamp: str
    sender: str
    command: str
    sensors: List[int] = list()
    leds: List[int] = list()

def main():
    DEBUG = True
    DEBUG = False
    with ArduinoThread(port=S.ARDUINO_PATH) as arduino:
        arduino.debug = DEBUG

        def get_respond():
            respond: Message = Message.model_validate_json(arduino.read())
            respond.timestamp = datetime.now().isoformat()
            return respond
        
        arduino.write_line("Hello world")
        while True:
            read_sensors = Message(command="read_sensors", sender="server", timestamp=datetime.now().isoformat())
            print(f"{read_sensors!r}")
            arduino.write_line(read_sensors.model_dump_json())
            
            time.sleep(1)

            respond = get_respond()
            print(f"{respond!r}")


if __name__ == "__main__":
    main()