from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    telegram_token: str = "replace_me"
    dummy_api_url: str = "https://httpbin.org/post"
    tmp_dir: Path = Path("./storage/tmp")
    log_level: str = "INFO"