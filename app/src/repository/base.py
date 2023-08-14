from typing import Generic, TypeVar

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
ReadSchemaType = TypeVar('ReadSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCRUDRepository(
    Generic[ModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]
):
    def __init__(
        self,
        model: type[ModelType],
        schema: type[ReadSchemaType],
        db_session: AsyncSession
    ):
        self.model = model
        self.schema = schema
        self.db_session = db_session

    def process_db_data(self, db_item: ModelType) -> ReadSchemaType:
        return self.schema.parse_obj(jsonable_encoder(db_item))

    async def get(self, id_: str, as_model=False) -> ReadSchemaType:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.db_session.execute(stmt)
        try:
            row = result.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__tablename__} not found'
            )
        return row if as_model else self.process_db_data(row)

    async def get_list(self, **kwargs) -> list[ReadSchemaType]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.db_session.execute(stmt)
        rows = result.scalars().all()
        return [self.process_db_data(row) for row in rows]

    async def create(self, obj_in: CreateSchemaType, **kwargs) -> ReadSchemaType:
        db_obj = self.model(**dict(**obj_in.dict(), **kwargs))
        self.db_session.add(db_obj)
        await self.db_session.commit()
        await self.db_session.refresh(db_obj)
        return self.process_db_data(db_obj)

    async def update(self, id_: str, obj_in: UpdateSchemaType) -> ReadSchemaType:
        db_obj = await self.get(id_=id_, as_model=True)
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db_session.add(db_obj)
        await self.db_session.commit()
        await self.db_session.refresh(db_obj)
        return self.process_db_data(db_obj)

    async def delete(self, id_: str) -> JSONResponse:
        db_obj = await self.get(id_=id_, as_model=True)
        await self.db_session.delete(db_obj)
        await self.db_session.commit()
        return JSONResponse(
            content={
                'status': True,
                'message': f'The {self.model.__tablename__} has been deleted'
            }
        )
