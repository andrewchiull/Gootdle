import time

from settings import S

from src.arduino.arduino import ArduinoThread

def main():
    with ArduinoThread(port=S.ARDUINO_PATH) as arduino:
        arduino.write_line("Hello world")
        while True:
            time.sleep(1)
            data = {"command": "read_sensors"} # TODO pydantic validation
            print(data)
            arduino.write_json(data)

if __name__ == "__main__":
    main()