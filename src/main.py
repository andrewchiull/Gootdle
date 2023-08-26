import argparse
# [argparse — Parser for command-line options, arguments and sub-commands — Python 3.11.4 documentation](https://docs.python.org/3.8/library/argparse.html#const)
# [Python argparse 用法與範例 | ShengYu Talk](https://shengyu7697.github.io/python-argparse/)

parser = argparse.ArgumentParser(description='Main function of the project of Google HPS 2023 Team 8. Created by Andrew Chiu.')
parser.add_argument('-d', '--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help="turn on debug mode (default: off); will set the logging level to 'DEBUG'")
parser.add_argument('-l', '--log', dest='log_level',
                    default="INFO", type=str,
                    help="set the logging level (default: 'INFO')")

args = parser.parse_args()

import os
os.environ["LOG_LEVEL"] = "DEBUG" if args.debug else args.log_level

import time
from time import sleep
from datetime import datetime
from settings import S, create_logger
log = create_logger(__file__, S.LOG_LEVEL)

from src.arduino.arduino import ArduinoThread, ArduinoControl, Message


THRESHOLD = 2000
SLEEP_SEC = 0.1


USING_0th = False

V_in = 1024
R_f = 10E+3
SCALE = 1E+6

def main():
    with ArduinoThread(port=S.ARDUINO_PORT) as arduino: # TODO What if arduino fails?
        arduino: ArduinoControl # NOT a ArduinoThread object!!!
        arduino.debug = S.DEBUG

        arduino.transport.serial.flush()
        arduino.buffer = bytearray()

        # [Step 1] Arduino responds that ARDUINO_IS_READY
        # [Step 2] Server waits until ARDUINO_IS_READY
        while True:
            # [Step 3] Server responds that SERVER_IS_READY
            if arduino.read_raw_data() == "ARDUINO_IS_READY":
                log.info("SERVER_IS_READY")
                break
            else:
                log.debug("Waiting for 'ARDUINO_IS_READY'...")
                sleep(SLEEP_SEC)
        
        # [Step 4] Arduino waits until server is ready
        # [Step 5] Server starts to send messages

        def get_respond(command: str):  # TODO very ugly
            raw_respond = arduino.read_raw_data()

            # Ignore
            if (raw_respond is None
                or raw_respond == "ARDUINO_IS_READY"
                or raw_respond.startswith("[[ECHO]]")
                or raw_respond.startswith("[[DEBUG]]")):
                log.debug(f"Ignore {raw_respond = }")
                return None

            try:
                respond: Message = Message.model_validate_json(raw_respond)
            except Exception as e:
                log.exception(e)
                return None
            respond.timestamp = datetime.now().isoformat()
 
            if respond.command != command:
                log.debug(f"Expected {command = }, but {respond.command = }")
                return None
            
            arduino.clear_raw_data()
            return respond
        
        def send_command(command, **kwarg):
            log.info(f"Send {command = }")
            msg = Message(command=command, sender="server", timestamp=datetime.now().isoformat(), **kwarg)
            arduino.write_line(msg.model_dump_json())

            while True:
                sleep(SLEEP_SEC)
                result = get_respond(command)
                if result:
                    log.debug(f"{result = !r}")
                    break

            return result

        while True:

            result = send_command("read_sensors")
            log.info(f"{result.sensors = }")

            sensors = [int(SCALE * (V_in-V_out)/(V_out*R_f)) 
                       for V_out in result.sensors]
            
            if not USING_0th: sensors[0] = None # Not used
            log.info(f"{sensors = }")
            sleep(SLEEP_SEC)

            def threshold(sensor: int) -> int:
                return int(sensor > THRESHOLD) if sensor else None

            leds = list(map(threshold, sensors))
            if not USING_0th: leds[0] = None # Not used


            result = send_command("write_leds", leds=leds)
            log.info(f"{result.leds = }")

            sleep(SLEEP_SEC)




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)