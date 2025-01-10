from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import DuplicateException
from app.api.validators import (
    check_invested_amount,
    check_name_duplicate,
    check_project_exists,
    check_project_open,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.utils import (
    patch_distribute_funds,
    get_uninvested_objects,
    update_charity_project_logic,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Создание нового благотворительного проекта",
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    unallocated_donations = await get_uninvested_objects(Donation, session)
    try:
        patch_distribute_funds(
            opened_items=unallocated_donations, funds=new_project
        )
        await session.commit()
        await session.refresh(new_project)
    except IntegrityError:
        await session.rollback()
        raise DuplicateException('Средства распределены')
    return new_project


@router.get(
    '/',
    response_model=Optional[List[CharityProjectDB]],
    response_model_exclude_none=True,
    summary="Получение всех благотворительных проектов",
)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Частичное обновление благотворительного проекта",
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exists(project_id, session)
    await check_project_open(project_id, session)

    return await update_charity_project_logic(
        charity_project, obj_in, project_id, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Удаление благотворительного проекта",
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление проектов - суперюзер."""
    charity_project = await check_project_exists(project_id, session)
    await check_invested_amount(project_id, session)
    return await charity_project_crud.remove(
        charity_project, session
    )
