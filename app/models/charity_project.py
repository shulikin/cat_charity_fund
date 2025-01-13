from sqlalchemy import (
    Column,
    String,
    Text
)

from app.core.config import Constant
from app.models.base import ProjectDonationBase


class CharityProject(ProjectDonationBase):
    """Модель благотворительного проекта.

    Наследуется от ProjectDonationBase и добавляет специфические поля
    для описания благотворительных проектов.
    """

    name = Column(
        String(Constant.NAME_MAX_LEN),
        unique=True, nullable=False
    )
    description = Column(
        Text,
        nullable=False
    )

    def __repr__(self):
        return (
            f'Проект {self.name}: {self.description}'
        )
