# [Develop a serial monitor with Python • AranaCorp](https://www.aranacorp.com/en/develop-a-serial-monitor-with-python/)

# %%
from serial.tools.list_ports import comports
usb_ports = [p.name for p in comports() if "tty" in p.name]
print(usb_ports)


# %%
