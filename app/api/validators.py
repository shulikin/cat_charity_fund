from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка на дублирование имени проекта.

    Проверяет, существует ли проект с таким именем в базе данных.
    Если проект найден, генерируется исключение с кодом ошибки 400.
    """
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект уже существует',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Получение благотворительного проекта по ID.

    Получения проекта с указанным ID. Если проект не найден,
    генерируется исключение с кодом ошибки 404.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_open(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка, открыт ли проект.

    Если проект закрыт (дата закрытия указана),
    генерируется исключение с кодом ошибки 400.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект закрыт, редактирование запрещено',
        )
    return charity_project


async def validate_update_project(
    obj_in,
    project_id: int,
    session: AsyncSession
) -> None:
    """Валидация данных для обновления благотворительного проекта.

    Args:
        obj_in (UpdateProjectSchema): Данные для обновления проекта.
        project_id (int): ID проекта для проверки.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Raises:
        ValueError: Если данные не прошли валидацию.
    """
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_investing_funds(project_id, obj_in.full_amount, session)


async def check_investing_funds(
        project_id: int,
        obj_in_full_amount,
        session: AsyncSession,
) -> CharityProject:
    """Проверка, вложена ли сумма в проект.

    Проверяет, не меньше ли сумма вложенных средств, чем текущая сумма проекта.
    Если текущая сумма меньше вложенной,
    генерируется исключение с кодом ошибки 400.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if obj_in_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма меньше вложенной!',
        )
    return charity_project


async def check_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка наличия вложенных средств в проекте.

    Проверяет, разрешение на удаление. Если средства уже вложены,
    генерируется исключение с кодом ошибки 400.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return charity_project
