import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from pydantic import (
    BaseSettings,
    EmailStr
)


class Constant:
    """Класс для хранения различных констант."""

    DEFAULT_INVESTED = 0
    NAME_MAX_LEN = 100
    NAME_MIN_LEN = 1
    BASE_DIR = Path(__file__).parent
    LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
    DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'


class Settings(BaseSettings):
    """Класс конфигурации."""

    app_title: str = 'Благотворительный фонд QRKot'
    app_description: str = 'Фонд собирает пожертвования на целевые проекты'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """Класс конфигурации '.env'."""

        env_file = '.env'


settings = Settings()


def configure_logging():
    """Функция настройки логирования."""
    log_dir = Constant.BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'qrkot.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 ** 6,
        backupCount=5
    )
    logging.basicConfig(
        datefmt=Constant.DATETIME_FORMAT,
        format=Constant.LOG_FORMAT,
        level=logging.INFO,
        handlers=(
            rotating_handler,
            logging.StreamHandler()
        )
    )
