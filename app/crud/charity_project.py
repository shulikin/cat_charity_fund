from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBaseAdvanced
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBaseAdvanced):
    """Класс для работы с операциями CRUD.

    Наследуется от CRUDBaseAdvanced и предоставляет дополнительные методы
    для работы с проектами.
    """

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Поиск по имени с использованием общего метода."""
        query = (select(CharityProject)
                 .where(CharityProject.name == project_name))
        result = await session.execute(query)
        return result.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
