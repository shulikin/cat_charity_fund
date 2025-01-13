from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_invested_amount,
    check_project_exists,
    check_project_open,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.utils import (
    process_new_charity_project,
    update_charity_project_logic,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создание нового благотворительного проекта',
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового благотворительного проекта.

    Позволяет суперпользователям создать новый
    благотворительный проект, предоставив необходимые данные о проекте.
    """
    return await process_new_charity_project(charity_project, session)


@router.get(
    '/',
    response_model=Optional[List[CharityProjectDB]],
    response_model_exclude_none=True,
    summary='Получение всех благотворительных проектов',
)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    """Получение всех благотворительных проектов.

    Возвращает все благотворительные проекты, хранящиеся в базе данных.
    Возвращает список проектов или пустой список, если проекты отсутствуют.
    """
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Частичное обновление благотворительного проекта',
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Частичное обновление благотворительного проекта.

    Позволяет суперпользователям частично обновить благотворительный
    проект, при этом проверяется, что проект существует и открыт.
    """
    charity_project = await check_project_exists(project_id, session)
    await check_project_open(project_id, session)

    return await update_charity_project_logic(
        charity_project, obj_in, project_id, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удаление благотворительного проекта',
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление благотворительного проекта.

    Позволяет суперпользователям удалить благотворительный проект после того,
    как будет проверено, что проект существует и в нем не было вложено средств.
    """
    charity_project = await check_project_exists(project_id, session)
    await check_invested_amount(project_id, session)
    return await charity_project_crud.remove(
        charity_project, session
    )
