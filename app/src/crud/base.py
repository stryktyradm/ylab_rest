from typing import Any, TypeVar, Generic, Type

from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], schema: Type[ReadSchemaType]):
        self.model = model
        self.schema = schema

    def process_data_from_db(self, item: ModelType) -> ReadSchemaType:
        return self.schema.parse_obj(jsonable_encoder(item))

    def get(self, db: Session, id_: Any, in_db: bool = False) -> ReadSchemaType | ModelType:
        db_obj = db.query(self.model).filter(self.model.id == id_).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__.lower()} not found"
            )
        if in_db:
            return db_obj
        item = self.process_data_from_db(db_obj)
        return item

    def get_list(self, db: Session, **kwargs: dict) -> list[ReadSchemaType]:
        db_obj_list = db.query(self.model).filter_by(**kwargs).all()
        item_list = [self.process_data_from_db(obj) for obj in db_obj_list]
        return item_list

    def create(self, db: Session, obj_in: CreateSchemaType, **kwargs: dict) -> ReadSchemaType:
        db_obj = self.model(**dict(**obj_in.dict(), **kwargs))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        item = self.process_data_from_db(db_obj)
        return item

    def update(self, db: Session, id_: Any, obj_in: UpdateSchemaType) -> ReadSchemaType:
        db_obj = self.get(db=db, id_=id_, in_db=True)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        item = self.process_data_from_db(db_obj)
        return item

    def delete(self, db: Session, id_: int):
        db_obj = self.get(db=db, id_=id_, in_db=True)
        db.delete(db_obj)
        db.commit()
        return JSONResponse(
            content={
                "status": True,
                "message": f"The {self.model.__name__.lower()} has been deleted"
            }
        )
