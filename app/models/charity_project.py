from sqlalchemy import (
    Column,
    String,
    Text
)

from app.core.config import Constant
from app.models.base import ProjectDonationBase


class CharityProject(ProjectDonationBase):

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
