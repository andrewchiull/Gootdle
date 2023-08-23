from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

# [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
class Settings(BaseSettings):
    # [Config - Pydantic](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.frozen)
    model_config = ConfigDict(frozen=True)

    ROOT_DIR: Path = Path(__file__).parent

S = Settings()


def create_logger(NAME: str):
    import logging
    import sys

    LEVEL = logging.INFO
    # NAME = Path(current_file).name
    FILE = S.ROOT_DIR / "logs" / (NAME + ".log")

    # TODO try logging.config
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    logger = logging.getLogger(NAME)
    logger.setLevel(LEVEL)

    file_handler = logging.FileHandler(filename=FILE, mode='a')
    file_handler.setLevel(LEVEL)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LEVEL)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger