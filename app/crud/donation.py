from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Класс для работы с операциями CRUD для пожертвований.

    Наследуется от CRUDBase и предоставляет дополнительные методы
    для работы с пожертвованиями.
    """

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> Optional[List[Donation]]:
        """Получить все пожертвования пользователя по его ID.

        Этот метод использует общий метод `get_by_kwargs`, чтобы найти все
        пожертвования, связанные с указанным пользователем.
        """
        return await self.get_by_kwargs(session, user_id=user.id)


donation_crud = CRUDDonation(Donation)
