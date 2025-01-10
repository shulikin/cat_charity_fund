from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> Optional[List[Donation]]:
        """Поиск по ID пользователя с использованием общего метода."""
        return await self.get_by_kwargs(session, user_id=user.id)


donation_crud = CRUDDonation(Donation)
