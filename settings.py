# %%
# TODO separate logging

import os
LOG_LEVEL = os.environ["LOG_LEVEL"]
print(f"{LOG_LEVEL = }")

from pathlib import Path
ROOT_PATH = Path(__file__).parent # Root of the project

def create_logger(file: str, level: str):
    import logging
    import sys
    module_path = Path(file).relative_to(ROOT_PATH)
    name = str(module_path.with_suffix('')).replace("/", ".")

    numeric_level: int = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % level)

    FILE = ROOT_PATH / "logs" / (name + ".log")

    # TODO try logging.config
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    file_handler = logging.FileHandler(filename=FILE, mode='a')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.debug(f"Logger {name} STARTS")
    logger.debug(f"The log file stores at: {FILE.absolute()}")
    return logger

log = create_logger(__file__, LOG_LEVEL)

from typing import Optional
import platform
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from serial import SerialException

# TODO Add a logger for different debug mode

# [Develop a serial monitor with Python • AranaCorp](https://www.aranacorp.com/en/
from serial.tools.list_ports import comports

def get_arduino_port():
    usb_ports = [p.name for p in comports() if ("tty" in p.name) or ("usb" in p.name)]
    
    try:
        port =  usb_ports[0]
        return "/dev/" + port
    except IndexError as e:
        log.exception(f"Arduino device is not found. Current usb ports: {usb_ports if usb_ports else None}.")
        # raise SerialException(f"Arduino device is not found. Current usb ports: {usb_ports if usb_ports else None}.")
        # import setting 的時候就會 raise，沒辦法在 main 接
        return None

"""
╭─ 19:09:13  andrewchiu@Andrew-MBP  ~/Google-HPS-2023-Team8   main ● ↑4 ⍟1 
╰─ ipython "/Users/andrewchiu/Google-HPS-2023-Team8/src/main.py"
2023-08-23 19:09:34,257 | settings | DEBUG | Logger settings STARTS
2023-08-23 19:09:34,408 | settings | ERROR | list index out of range
Traceback (most recent call last):
File "/Users/andrewchiu/Google-HPS-2023-Team8/settings.py", line 54, in get_arduino_port
    port =  usb_ports[0]
IndexError: list index out of range
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
~/Google-HPS-2023-Team8/settings.py in get_arduino_port()
    53     try:
---> 54         port =  usb_ports[0]
    55         return port

IndexError: list index out of range

During handling of the above exception, another exception occurred:

SerialException                           Traceback (most recent call last)
~/Google-HPS-2023-Team8/src/main.py in <module>
    5 from pydantic import BaseModel
    6 from pydantic_core import ValidationError
----> 7 from settings import create_logger
    8 log = create_logger(__file__, "DEBUG")
    9 # from settings import S

~/Google-HPS-2023-Team8/settings.py in <module>
    59 
    60 # [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
---> 61 class Settings(BaseSettings):
    62     # [Config - Pydantic](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.frozen)
    63     model_config = ConfigDict(frozen=True)

~/Google-HPS-2023-Team8/settings.py in Settings()
    66     ROOT: Path = ROOT_PATH
    67     OS: str = platform.system()
---> 68     ARDUINO_PORT: Optional[str] = get_arduino_port()
    69 
    70     VIDEO_SOURCE: str = str(ROOT/"src/cv/test_input_video/fisheye.MOV")

~/Google-HPS-2023-Team8/settings.py in get_arduino_port()
    56     except IndexError as e:
    57         log.exception(e)
---> 58         raise SerialException(f"Arduino device is not found. Current usb ports: {usb_ports if usb_ports else None}.")
    59 
    60 # [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)

SerialException: Arduino device is not found. Current usb ports: None.
"""

# [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
class Settings(BaseSettings):
    # [Config - Pydantic](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.frozen)
    model_config = ConfigDict(frozen=True)
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True if LOG_LEVEL == "DEBUG" else False
    ROOT: Path = ROOT_PATH
    OS: str = platform.system()
    ARDUINO_PORT: Optional[str] = get_arduino_port()
    VIDEO_SOURCE: str = str(ROOT/"src/cv/test_input_video/fisheye.MOV")
    # VIDEO_SOURCE: str = str(ROOT/"src/cv/test_input_video/white_tshirt.MOV")
    SLOTS_SIZE: int = 5


    # [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
    # [Manage sensitive data with Docker secrets | Docker Documentation](https://docs.docker.com/engine/swarm/secrets/)
    model_config = SettingsConfigDict(secrets_dir=ROOT/'run/secrets')

    DB_USERNAME: str
    DB_PASSWORD: str



# %%
try:
    S = Settings()
    # pass
except Exception as e:
    log.exception(e)