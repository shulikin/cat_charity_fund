from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения данных пользователя.

    Расширяет базовую схему пользователя
    с использованием целочисленного идентификатора.
    """


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания нового пользователя.

    Включает обязательные поля, такие как email и пароль.
    """


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления информации о пользователе.

    Поддерживает частичное обновление данных.
    """
