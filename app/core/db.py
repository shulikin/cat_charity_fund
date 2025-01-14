from typing import AsyncGenerator
from sqlalchemy import (
    Column,
    Integer
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    sessionmaker
)

from app.core.config import settings


class PreBase:
    """Базовый класс для всех моделей.

    Этот класс используется для автоматической генерации имени таблицы
    (по имени модели в нижнем регистре)
    и добавления общего поля `id` в каждую модель.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True
    )


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии для работы с базой данных.

    Этот генератор создает сессию, используя
    `AsyncSessionLocal`, и автоматически
    управляет её жизненным циклом (открытие и закрытие).
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
