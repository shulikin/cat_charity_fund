from datetime import datetime
from typing import List, Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation
from app.api.validators import check_name_duplicate, check_investing_funds

AllocatableResource = Union[Donation, CharityProject]


def patch_distribute_funds(
        opened_items: Optional[List[AllocatableResource]],
        funds: AllocatableResource,
) -> AllocatableResource:
    if opened_items:
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
    item.fully_invested = True
    item.close_date = datetime.now()
    return item


async def get_uninvested_objects(
        obj_model: Type[AllocatableResource],
        session: AsyncSession,
) -> Optional[List[AllocatableResource]]:
    uninvested_objects = await session.execute(
        select(obj_model).where(
            obj_model.fully_invested == 0
        ).order_by(obj_model.create_date)
    )
    return uninvested_objects.scalars().all()


async def update_charity_project_logic(
    charity_project, obj_in, project_id: int, session: AsyncSession
):
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_investing_funds(project_id, obj_in.full_amount, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    if obj_in.full_amount == charity_project.invested_amount:
        close_item(charity_project)

    return charity_project
