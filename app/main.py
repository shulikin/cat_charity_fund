import logging

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import configure_logging, settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """Выполняет действия при запуске приложения.

    Создает первого суперпользователя и настраивает логирование.
    """
    await create_first_superuser()
    configure_logging()
    logging.info('Сервис запущен')


@app.on_event('shutdown')
async def shutdown_event():
    """Выполняет действия при остановке приложения.

    Логирует факт завершения работы сервиса.
    """
    logging.info('Сервис остановлен')
