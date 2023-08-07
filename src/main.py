import time
from time import sleep
from datetime import datetime
from typing import List
from pydantic import BaseModel
from pydantic_core import ValidationError
from settings import S

from src.arduino.arduino import ArduinoThread, ArduinoControl

class Message(BaseModel):
    timestamp: str
    sender: str
    command: str
    sensors: List[int] = list()
    leds: List[int] = list()


THRESHOLD = 2000
SLEEP_SEC = 0.2
DEBUG = True

V_in = 1024
R_f = 10E+3
SCALE = 1E+6

def threshold(sensor: int) -> int:
    return int(sensor > THRESHOLD)

def main():
    with ArduinoThread(port=S.ARDUINO_PATH) as arduino:
        arduino: ArduinoControl # NOT a ArduinoThread object!!!
        arduino.debug = DEBUG


        arduino.transport.serial.dtr = False
        # FLUSH ANYTHING
        arduino.transport.serial.flush()
        arduino.transport.serial.dtr = True
        arduino.buffer = bytearray()

        try:
            # [Step 1] Arduino responds that ARDUINO_IS_READY
            # [Step 2] Server waits until ARDUINO_IS_READY
            while True:
                CONNECTION_MADE = arduino.read()
                print(f"{CONNECTION_MADE = !r}")

                # [Step 3] Server responds that SERVER_IS_READY
                if CONNECTION_MADE == "ARDUINO_IS_READY":
                    arduino.write_line("SERVER_IS_READY")
                    break
                else:
                    print("Waiting for 'ARDUINO_IS_READY'...")
                    sleep(SLEEP_SEC)
                    
                    # raise ConnectionError(f"[ERROR] {CONNECTION_MADE = }")

        except ConnectionError as e:
            print(e)
        
        # [Step 4] Arduino waits until server is ready
        # [Step 5] Server starts to send messages

        def get_respond(command):  # TODO very ugly
            raw_respond = arduino.read()
            
            # Ignore the initial state
            if raw_respond == "ARDUINO_IS_READY":
                return None

            # Ignore echos
            if raw_respond.startswith("[[ECHO]]"):
                return None

            try:
                respond: Message = Message.model_validate_json(raw_respond)
                
                if respond.command != command:
                    print(f"{respond.command=} != {command=}")
                    raise ValidationError
            except ValidationError as e:
            # except Exception as e:
                print(e)
                return None
            respond.timestamp = datetime.now().isoformat()
            return respond
        
        def command(command, **kwarg):
            msg = Message(command=command, sender="server", timestamp=datetime.now().isoformat(), **kwarg)
            arduino.write_line(msg.model_dump_json())

        # arduino.write_line("Hello world")
        while True:
            # if arduino.read() == "ARDUINO_IS_IDLE":
            #     sleep(SLEEP_SEC)
            #     continue

            command("read_sensors")
            while True:
                sleep(SLEEP_SEC)
                read_sensors_respond = get_respond("read_sensors")
                if read_sensors_respond:
                    break

            # print(f"{read_sensors_respond!r}")
            sensors = [ int(SCALE * (V_in-V_out)/(V_out*R_f)) for V_out in read_sensors_respond.sensors]
            print(sensors)
            print()
            
            sleep(SLEEP_SEC)
            
            
            
            leds = list()
            for sensor in read_sensors_respond.sensors:
                leds.append(threshold(sensor))
            
            
            # leds = list()
            # for sensor in read_sensors_respond.sensors:
            #     leds.append(int(weight(sensor) > THRESHOLD))

            # leds = list()
            # for sensor in read_sensors_respond.sensors:
            #     leds.append(int(weight(sensor) > THRESHOLD))
            
            command("write_leds", leds=leds)
            
            while True:
                sleep(SLEEP_SEC)
                write_leds_respond = get_respond("write_leds")
                if write_leds_respond:
                    print(f"{write_leds_respond!r}")
                    break

            sleep(SLEEP_SEC)
            
            



if __name__ == "__main__":
    main()