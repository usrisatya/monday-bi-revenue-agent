from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MONDAY_API_KEY: str
    DEALS_BOARD_ID: str
    WORK_ORDERS_BOARD_ID: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()