from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

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
    ) -> Optional[CharityProject]:
        """Поиск по имени с использованием общего метода."""
        return await self.get_by_kwargs(session, name=project_name)


charity_project_crud = CRUDCharityProject(CharityProject)
