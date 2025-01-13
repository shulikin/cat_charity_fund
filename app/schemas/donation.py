from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import Constant


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""

    full_amount: PositiveInt = Field(
        ...,
        title='Сумма пожертвования'
    )
    comment: Optional[str] = Field(
        None,
        title='Комментарий к пожертвованию'
    )

    class Config:
        """Конфигурация базовой схемы пожертвования."""

        title = 'Базовая схема пожертвования'


class DonationCreate(DonationBase):
    """Схема для создания нового пожертвования."""

    class Config:
        """Конфигурация для создания пожертвования."""

        extra = Extra.forbid  # Запрещаем дополнительные поля
        title = 'Создание пожертвования'


class DonationDB(DonationBase):
    """Схема данных пожертвования из базы, доступная пользователю."""

    id: int = Field(
        ...,
        title='ID пожертвования'
    )
    create_date: datetime = Field(
        ...,
        title='Дата создания'
    )

    class Config:
        """Конфигурация данных пожертвования."""

        title = 'Данные пожертвования'
        orm_mode = True


class DonationDBSuper(DonationDB):
    """Расширенная схема данных пожертвования для внутреннего использования."""

    user_id: Optional[int] = Field(
        None,
        title='ID пользователя'
    )
    invested_amount: int = Field(
        Constant.DEFAULT_INVESTED,
        title='Инвестированная сумма'
    )
    fully_invested: bool = Field(
        False,
        title='Полностью инвестировано'
    )
    close_date: Optional[datetime] = Field(
        None,
        title='Дата закрытия'
    )

    class Config:
        """Конфигурация расширенной схемы данных пожертвования."""

        title = 'Расширенные данные пожертвования'
        orm_mode = True
