
# [Raspberry Pi Arduino Serial Communication - Everything You Need To Know - The Robotics Back-End](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)

import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/tty.usbmodem1411201', 9600, timeout=0.1)
    ser.reset_input_buffer()

    greeting =  "Connecting to Arduino..."
    ser.write(f"{greeting}\n".encode('utf-8'))

    count_try = 0
    while True:
        count_try += 1
        ser.write(f"{greeting}\n".encode('utf-8'))
        print(f"{greeting} [{count_try}]")
        try:
            respond = ser.readline().decode('utf-8').rstrip()
        except UnicodeDecodeError:
            pass
        if greeting in respond:
            print(f"Arduino responds: {respond}")
            print("Successfully connected to Arduino!\n")

            break
        time.sleep(1/5)

    i = 0
    while True:
        command = input("Enter the command: ")
        ser.write(f"{command}\n".encode('utf-8'))

        while True:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "":
                break
            print(f">>> {line}")
        print()
        time.sleep(1/5)
