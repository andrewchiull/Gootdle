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

from time import sleep
from settings import S, create_logger
log = create_logger(__file__, S.LOG_LEVEL)

from src.arduino.arduino import ArduinoThread, ArduinoControl


THRESHOLD = {
    1: 500,
    2: 2000,
    3: 2000,
    4: 2000,
    5: 2000,
}

class LedColor():
    # TODO use hex
    R = [255,0,0]
    G = [0,255,0]
    B = [0,0,255]
    C = [0,255,255]
    M = [255,0,255]
    Y = [255,255,0]
    K = [0,0,0]
    W = [255,255,255]

SLEEP_SEC = 0.1

V_in = 1024
R_f = 10E+3
SCALE = 1E+6

def main():
    import cv2 # for waitKey
    cv2.imshow("nothing", S.EMPTY_IMAGE)
    with ArduinoThread(port=S.ARDUINO_PORT) as arduino: # TODO What if arduino fails?
        arduino: ArduinoControl # NOT a ArduinoThread object!!!
        arduino.initialize()
        
        # DEMO_MODE = False
        DEMO_MODE = True

        while True:
            c = LedColor()
            if DEMO_MODE:
                log.info(f"{DEMO_MODE = }")
                def show_colors(colors: str):
                    leds = list()
                    for color in colors[:S.SLOTS_SIZE]:
                        leds.append(getattr(c, color))
                        leds.append(getattr(c, color))
                    log.info(colors)
                    log.info(leds)
                    arduino.send_command("write_leds", leds=leds)


                # Opening
                RAINBOW = "RYGCBMRYGCBM"
                steps = [
                    RAINBOW[0:], # waiting
                    # RAINBOW[1:], # waiting
                    # RAINBOW[2:], # waiting
                    # RAINBOW[3:], # waiting
                    # RAINBOW[4:], # waiting
                ]
                
                for step in steps:
                    show_colors(step)

                # # waiting
                # i = 0
                # while True:
                #     i += 1
                #     show_colors(steps[i % 5])
                #     if cv2.waitKey(1) & 0xFF == 27:  # 按下"esc"键
                #         break


                show_colors("KKKKK")
                cv2.waitKey(0)


                # 1
                show_colors("WKKKK")
                # cv2.waitKey(0)

                # pending
                RAINBOW = "GKKKKGKKKK"
                steps = [
                    # RAINBOW[0:], # waiting
                    RAINBOW[1:], # waiting
                    RAINBOW[2:], # waiting
                    RAINBOW[3:], # waiting
                    RAINBOW[4:], # waiting
                    RAINBOW[5:], # waiting
                ]
                for step in steps:
                    step = 'W' + step
                    show_colors(step)
                    # time.sleep(0.05)
                
                # 1
                show_colors("WKKKK")
                cv2.waitKey(0)
                
                # 1, 5
                show_colors("WKKKW")
                cv2.waitKey(0)
                
                # NO
                show_colors("KKKKK")

                
                break
                
            # result = arduino.send_command("read_sensors")
            # log.info(f"{result.sensors = }")

            # # Convert readings
            # readings = [int(SCALE * (V_in-V_out)/(V_out*R_f)) 
            #            for V_out in result.sensors]
            
            # # Ignore sensor #0
            # readings[0] = None
            # log.info(f"{readings = }")
            # sleep(SLEEP_SEC)

            # def threshold(i: int ,reading: int) -> int:
            #     return int(reading > THRESHOLD[i])


            # leds = list()
            # # 2 leds for each sensor, e.g.:
            # # sensor #0 -> (ignored)
            # # sensor #1 -> led #0, #1
            # # sensor #2 -> led #2, #3
            # # sensor #3 -> led #4, #5
            # # sensor #4 -> led #6, #7
            # # sensor #5 -> led #8, #9
            # for i, reading in enumerate(readings):
            #     if i == 0:
            #         # Ignore sensor #0
            #         continue
            #     high_or_low = threshold(i, reading) * 255
            #     leds.append([high_or_low, high_or_low, high_or_low])
            #     leds.append([high_or_low, high_or_low, high_or_low])


            # result = arduino.send_command("write_leds", leds=leds)
            # log.info(f"{result.leds = }")

            # sleep(SLEEP_SEC)




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)