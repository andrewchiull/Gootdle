from pathlib import Path
import platform
from attr import define

@define(frozen=True)
class Settings:
    ROOT: Path = Path(__file__).parent # Root of the project
    OS: str = platform.system()
    ARDUINO_PATH: Path = (Path("/dev/ttyACM0") if OS == "Linux" # docker or RPi
                    else Path("/dev/tty.usbmodem1411201")) # "Darwin" (macOS)