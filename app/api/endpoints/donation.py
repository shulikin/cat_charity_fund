from typing import (
    List,
    Optional
)

from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import (
    current_superuser,
    current_user
)
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationDBSuper
)

from app.services.utils import process_new_donation

router = APIRouter()


@router.post('/', response_model=DonationDB, response_model_exclude_none=True)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Создание новой пожертвования.

    Позволяет пользователям создавать пожертвования
    для благотворительных проектов.
    Пожертвование привязывается к текущему пользователю.
    """
    return await process_new_donation(donation, session, user)


@router.get(
    '/',
    response_model=Optional[List[DonationDBSuper]],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Получение всех пожертвований.

    Позволяет суперпользователям просматривать все пожертвования,
    сделанные пользователями.
    Если пожертвования отсутствуют, возвращается пустой список.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=Optional[List[DonationDB]],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение пожертвований текущего пользователя.

    Позволяет пользователю просматривать свои собственные пожертвования.
    Если пожертвования отсутствуют, возвращается пустой список.
    """
    return await donation_crud.get_by_user(user=user, session=session)
