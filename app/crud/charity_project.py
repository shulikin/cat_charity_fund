from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBaseAdvanced
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBaseAdvanced):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Поиск по имени с использованием общего метода."""
        projects = await self.get_by_kwargs(session, name=project_name)
        return projects[0].id if projects else None


charity_project_crud = CRUDCharityProject(CharityProject)
