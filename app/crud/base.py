from typing import Optional, List, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

T = TypeVar('T')  # Тип для модели


class CRUDBase:
    """Базовый класс для операций CRUD с моделью."""

    def __init__(self, model: Type[T]):
        """Инициализация CRUDBase."""
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[T]:
        """Получить все объекты модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: T,
            session: AsyncSession,
            user: Optional[User] = None,
    ) -> T:
        """Создать новый объект в базе данных."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_kwargs(
            self,
            session: AsyncSession,
            **kwargs,
    ) -> List[T]:
        """Получить объекты по произвольным ключевым аргументам."""
        query = select(self.model).filter_by(**kwargs)
        db_objs = await session.execute(query)
        return db_objs.scalars().all()


class CRUDBaseAdvanced(CRUDBase):
    """Расширенный класс для операций CRUD.

    Поддерживающий получение, обновление и удаление объектов.
    Наследуется от `CRUDBase`.
    """

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[T]:
        """Получить объект по его ID."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def update(
            self,
            db_obj: T,
            obj_in: T,
            session: AsyncSession,
    ) -> T:
        """Обновить объект в базе данных."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: T,
            session: AsyncSession,
    ) -> T:
        """Удалить объект из базы данных."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
