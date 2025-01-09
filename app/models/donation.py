from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text
)

from app.models.base import ProjectDonationBase


class Donation(ProjectDonationBase):

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пожертвований {self.full_amount} '
            f'комментариев {self.comment}'
        )
