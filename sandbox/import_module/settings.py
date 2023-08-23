from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

# [Settings Management - Pydantic](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
class Settings(BaseSettings):
    # [Config - Pydantic](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.frozen)
    model_config = ConfigDict(frozen=True)

    ROOT_DIR: Path = Path(__file__).parent

S = Settings()




