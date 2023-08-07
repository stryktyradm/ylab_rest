from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.repository.base import (
    BaseCRUDRepository,
    CreateSchemaType,
    ModelType,
    UpdateSchemaType,
)
from src.repository.cache import BaseCacheRepository

ReadSchemaType = TypeVar('ReadSchemaType', bound=BaseModel)


class BaseService(Generic[CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        repo: BaseCRUDRepository,
        schema: type[ReadSchemaType],
        cache: BaseCacheRepository,
        cache_namespace: str,
        linked_cache_namespace: list
    ):
        self.repo = repo
        self.cache = cache
        self.schema = schema
        self.cache_namespace = cache_namespace
        self.linked_cache_namespace = linked_cache_namespace

    def process_db_data(self, db_item: ModelType) -> ReadSchemaType:
        return self.schema.parse_obj(jsonable_encoder(db_item))

    async def get_item(self, id_: str) -> ReadSchemaType:
        item = await self.cache.get(id_)
        if not item:
            db_obj = await self.repo.get(id_=id_)
            item = self.process_db_data(db_obj)
            await self.cache.add(id_, jsonable_encoder(item))
        return item

    async def list_items(self, **kwargs) -> list[ReadSchemaType]:
        items = await self.cache.get(self.cache_namespace)
        if not items:
            db_objs = await self.repo.get_list(**kwargs)
            items = [self.process_db_data(db_obj) for db_obj in db_objs]
            await self.cache.add(self.cache_namespace, jsonable_encoder(items))
        return items

    async def create_item(self, obj_in: CreateSchemaType, **kwargs) -> ReadSchemaType:
        db_obj = await self.repo.create(obj_in=obj_in, **kwargs)
        item = self.process_db_data(db_obj)
        await self.cache.multi_clear(
            [self.cache_namespace, *self.linked_cache_namespace, *kwargs.values()]
        )
        await self.cache.add(item.id, jsonable_encoder(item))
        return item

    async def update_item(self, id_: str, obj_in: UpdateSchemaType) -> ReadSchemaType:
        db_obj = await self.repo.update(id_=id_, obj_in=obj_in)
        item = self.process_db_data(db_obj)
        await self.cache.add(id_, jsonable_encoder(item))
        await self.cache.clear(self.cache_namespace)
        return item

    async def delete_item(self, id_: str, **kwargs) -> JSONResponse:
        item = await self.repo.delete(id_=id_)
        await self.cache.multi_clear(
            [id_, self.cache_namespace, *self.linked_cache_namespace, *kwargs.values()]
        )
        return item
