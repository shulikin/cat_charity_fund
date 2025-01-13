import logging
from typing import Optional, Union, AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(
    session: AsyncSession = Depends(get_async_session)
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """Функция для получения экземпляра SQLAlchemyUserDatabase.

    Асинхронная сессия базы данных.
    База данных пользователей.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Создаёт и возвращает стратегию JWT для аутентификации.

    Стратегия JWT с заданными секретом и временем жизни.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Класс для управления пользователями.

    Наследует функции работы с пользователями от BaseUserManager
    и добавляет логику для валидации пароля и обработки событий регистрации.
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Проверяет, что пароль соответствует требованиям."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Минимум три символа'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Не может быть e-mail'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ) -> None:
        """Логирует событие регистрации пользователя."""
        logging.info(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(
    user_db=Depends(get_user_db)
) -> AsyncGenerator[UserManager, None]:
    """Возвращает менеджер пользователей для работы с базой данных."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
