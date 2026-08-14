import os
import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# 版本號的唯一來源，刻意不放進 ServerConfig：它由 release 流程改寫
# （.pr-quality.json 的 versioning.files 指向這一行），不接受環境變數覆寫，
# 否則部署出去的版本字串可能與 git tag 不一致。
APP_VERSION = "0.1.1"


def _resolve_env_file() -> str | None:
    """決定應使用的環境設定檔路徑。

    優先順序：
    1. 環境變數 APP_ENV_FILE
    2. 專案根目錄的 .env（若存在）
    3. 指令列第一個參數（若提供）
    """
    env_file = os.environ.get("APP_ENV_FILE")
    if env_file:
        return env_file

    dotenv_path = Path(".env")
    if dotenv_path.exists():
        return str(dotenv_path)

    if len(sys.argv) > 1:
        return sys.argv[1]

    return None


class ServerConfig(BaseSettings):
    # App
    APP_NAME: str = "fastapi-frame"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEV: bool = False
    DEBUG_LOG: bool = False
    AUTO_CREATE_TABLES: bool = False
    CORS_ORIGINS: list[str] = ["*"]

    # PostgreSQL
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi_frame"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(
        env_file=_resolve_env_file(),
        env_file_encoding="utf-8",
        validate_assignment=True,
        extra="ignore",
    )


SERVER_CONFIG = ServerConfig()
