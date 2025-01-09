from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.config import Constant
from app.core.db import Base


class ProjectDonationBase(Base):
    """Базовая абстрактная модель родителя
    для моделей проекта и пожертвования."""
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer,
        nullable=False,
        default=Constant.DEFAULT_INVESTED,
    )
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
