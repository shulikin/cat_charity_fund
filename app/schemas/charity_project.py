from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Extra,
    Field,
    PositiveInt,
    validator
)

from app.core.config import Constant


class CharityProjectBase(BaseModel):
    """Базовое схема объекта проекта."""
    name: Optional[str] = Field(
        None,
        title='Название',
        min_length=Constant.NAME_MIN_LEN,
        max_length=Constant.NAME_MAX_LEN,
    )
    description: Optional[str] = Field(None, title='Описание')
    full_amount: Optional[PositiveInt] = Field(None, title='Требуемая сумма')

    class Config:
        title = 'Базовая схема проекта'


class CharityProjectUpdate(CharityProjectBase):
    """Схема проекта."""

    class Config:
        title = 'Схема проекта'
        orm_mode = True
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "name": "string",
                "description": "string",
                "full_amount": 0
            }
        }

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    """Схема проекта для создания."""
    name: str = Field(
        ...,
        title='Название',
        min_length=Constant.NAME_MIN_LEN,
        max_length=Constant.NAME_MAX_LEN,
    )
    description: str = Field(..., title='Описание')
    full_amount: PositiveInt = Field(..., title='Требуемая сумма')

    class Config:
        title = 'Схема проекта для создания'
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    """Схема проекта для получения."""
    id: int = Field(..., title='Порядковый номер')
    invested_amount: int = Field(
        Constant.DEFAULT_INVESTED,
        title='Сколько пожертвовано',
    )
    fully_invested: bool = Field(False, title='Собрана нужная сумма')
    create_date: datetime = Field(..., title='Дата открытия проекта')
    close_date: Optional[datetime] = Field(None, title='Дата закрытия проекта')

    class Config:
        title = 'Схема проекта для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                "name": "string",
                "description": "string",
                "full_amount": 0,
                "id": 0,
                "invested_amount": 0,
                "fully_invested": 0,
                "create_date": "2019-08-24T14:15:22Z",
                "close_date": "2019-08-24T14:15:22Z"
            }
        }
