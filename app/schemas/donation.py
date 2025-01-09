from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import Constant


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""
    full_amount: PositiveInt = Field(..., title='Сумма')
    comment: Optional[str] = Field(None, title='Комментарий')

    class Config:
        title = 'Cхема'


class DonationCreate(DonationBase):
    """Схема пожертвования - создание."""

    class Config:
        extra = Extra.forbid
        title = 'Схема пожертвования'
        schema_extra = {
            'example': {
                "full_amount": 0,
                "comment": "string"
            }
        }


class DonationDB(DonationBase):
    """Схема пожертвования из базы - пользователем."""
    id: int = Field(..., title='ID пожертвования')
    create_date: datetime = Field(..., title='Дата')

    class Config:
        title = 'Схема'
        orm_mode = True
        schema_extra = {
            'example': {
                "full_amount": 0,
                "comment": "string",
                "id": 0,
                "create_date": "2019-08-24T14:15:22Z"
            }
        }


class DonationDBSuper(DonationDB):
    """Схема пожертвования из базы - суперпользователем."""
    user_id: Optional[int] = Field(None, title='ID пользователя')
    invested_amount: int = Field(
        Constant.DEFAULT_INVESTED,
        title='Сумма',
    )
    fully_invested: bool = Field(False, title='Итого сумма')
    close_date: Optional[datetime] = Field(None, title='Дата')

    class Config:
        title = 'Пожертвование'
        orm_mode = True
        schema_extra = {
            'example': {
                "full_amount": 0,
                "comment": "string",
                "id": 0,
                "create_date": "2019-08-24T14:15:22Z",
                "user_id": 0,
                "invested_amount": 0,
                "fully_invested": 0,
                "close_date": "2019-08-24T14:15:22Z"
            }
        }
