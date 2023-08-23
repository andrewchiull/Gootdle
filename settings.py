# %%

from pathlib import Path
import platform
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from serial import SerialException

# TODO Add a logger for different debug mode

# [Develop a serial monitor with Python • AranaCorp](https://www.aranacorp.com/en/
from serial.tools.list_ports import comports
def get_arduino_port():
    usb_ports = [p.name for p in comports() if "tty" in p.name]
    try:
        return usb_ports[0]
    except IndexError:
        raise SerialException(f"Arduino device is not found. Current usb ports: {usb_ports if usb_ports else None}.")

# [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
class Settings(BaseSettings):
    model_config = ConfigDict(frozen=True)
    # [Config - Pydantic](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.frozen)

    DEBUG: bool = False
    ROOT: Path = Path(__file__).parent # Root of the project
    OS: str = platform.system()
    ARDUINO_PORT: str = get_arduino_port()

    VIDEO_SOURCE: str = str(ROOT/"src/cv/test_input_video/fisheye.MOV")
    # VIDEO_SOURCE: str = str(ROOT/"src/cv/test_input_video/white_tshirt.MOV")


    # [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
    # [Manage sensitive data with Docker secrets | Docker Documentation](https://docs.docker.com/engine/swarm/secrets/)
    model_config = SettingsConfigDict(secrets_dir=ROOT/'run/secrets')

    DB_USERNAME: str
    DB_PASSWORD: str

# %%

S = Settings()

# %%