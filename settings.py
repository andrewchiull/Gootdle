# %%

from pathlib import Path
import yaml
import platform
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(frozen=True)
    # [Config - Pydantic](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.frozen)

    ROOT: Path = Path(__file__).parent # Root of the project
    OS: str = platform.system()
    ARDUINO_PATH: str = ("/dev/ttyACM0" if OS == "Linux" # docker or RPi
                    else "/dev/tty.usbmodem1411201") # "Darwin" (macOS)

    VIDEO_SOURCE: str = str(ROOT/"src/cv/test_input_video/white_tshirt.MOV")


    # [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
    # [Manage sensitive data with Docker secrets | Docker Documentation](https://docs.docker.com/engine/swarm/secrets/)
    model_config = SettingsConfigDict(secrets_dir=ROOT/'run/secrets')

    DB_USERNAME: str
    DB_PASSWORD: str

# %%

S = Settings()

# %%