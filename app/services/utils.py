from datetime import datetime
from typing import List, Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import DuplicateException
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation
from app.api.validators import check_name_duplicate, validate_update_project
from app.schemas.donation import DonationCreate

AllocatableResource = Union[Donation, CharityProject]


def patch_distribute_funds(
        opened_items: Optional[List[AllocatableResource]],
        funds: AllocatableResource,
) -> AllocatableResource:
    """Распределяет средства на список открытых элементов `opened_items`.

    Эта функция проверяет, сколько средств осталось у объекта `funds`,
    и распределяет их между открытыми элементами в `opened_items`.
    Если средств достаточно, элементы закрываются.
    """
    for item in opened_items:
        funds_diff = funds.full_amount - funds.invested_amount
        item_diff = item.full_amount - item.invested_amount
        if funds_diff >= item_diff:
            funds.invested_amount += item_diff
            item.invested_amount = item.full_amount
            close_item(item)
            if funds_diff == item_diff:
                close_item(funds)
        else:
            item.invested_amount += funds_diff
            funds.invested_amount = funds.full_amount
            close_item(funds)
            break
    return funds


def close_item(item: AllocatableResource) -> AllocatableResource:
    """Закрывает элемент, устанавливая флаги `fully_invested` и `close_date`.

    Эта функция обновляет флаг `fully_invested`
    и устанавливает дату закрытия для элемента.
    """
    item.fully_invested = True
    item.close_date = datetime.now()
    return item


async def get_uninvested_objects(
        obj_model: Type[AllocatableResource],
        session: AsyncSession,
) -> Optional[List[AllocatableResource]]:
    """Получает список объектов, которые ещё не инвестированы.

    Эта функция выполняет запрос в базу данных для получения всех объектов,
    которые не были полностью инвестированы.
    """
    uninvested_objects = await session.execute(
        select(obj_model).where(
            obj_model.fully_invested == 0
        ).order_by(obj_model.create_date)
    )
    return uninvested_objects.scalars().all()


async def update_charity_project_logic(
    charity_project, obj_in, project_id: int, session: AsyncSession
) -> CharityProject:
    """Логика обновления благотворительного проекта.

    Эта функция обновляет данные проекта в базе и проверяет,
    нужно ли его закрыть после обновления.
    """
    await validate_update_project(obj_in, project_id, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if obj_in.full_amount == charity_project.invested_amount:
        close_item(charity_project)

    return charity_project


async def distribute_funds(
    opened_items,
    funds,
    session
) -> None:
    """Функция для распределения средств и коммита в базе данных."""
    try:
        patch_distribute_funds(
            opened_items=opened_items,
            funds=funds
        )
        await session.commit()
        await session.refresh(funds)
    except IntegrityError:
        await session.rollback()
        raise DuplicateException('Средства распределены')


async def process_new_charity_project(
    charity_project,
    session: AsyncSession
) -> CharityProject:
    """Обрабатывает создание нового проекта.

    Проверяет уникальность имени проекта.
    Создает проект в базе данных.
    Распределяет нераспределенные пожертвования на новый проект.
    """
    await check_name_duplicate(
        charity_project.name,
        session
    )
    new_project = await charity_project_crud.create(
        charity_project,
        session
    )
    unallocated_donations = await get_uninvested_objects(
        Donation,
        session
    )
    await distribute_funds(
        unallocated_donations,
        new_project,
        session
    )

    return new_project


async def process_new_donation(
        donation: DonationCreate,
        session: AsyncSession,
        user
) -> Donation:
    """Обрабатывает создание нового пожертвования.

    Создает пожертвование в базе данных.
    Распределяет средства пожертвования на открытые проекты.
    """
    new_donation = await donation_crud.create(
        donation,
        session,
        user
    )
    open_projects = await get_uninvested_objects(
        CharityProject,
        session
    )
    await distribute_funds(
        open_projects,
        new_donation,
        session
    )
    return new_donation
