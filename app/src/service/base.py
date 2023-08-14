from typing import Generic, TypeVar

from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.repository.base import (
    BaseCRUDRepository,
    CreateSchemaType,
    ReadSchemaType,
    UpdateSchemaType,
)
from src.repository.cache import BaseCacheRepository

CRUDRepositoryType = TypeVar('CRUDRepositoryType', bound=BaseCRUDRepository)


class BaseService(Generic[CRUDRepositoryType, CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        repo: type[CRUDRepositoryType],
        schema: type[ReadSchemaType],
        cache: BaseCacheRepository,
        cache_mask: str,
        cache_root: str,
        cache_namespace: str,
    ):
        self.repo = repo
        self.schema = schema
        self.cache = cache
        self.cache_mask = cache_mask
        self.cache_root = cache_root
        self.cache_namespace = cache_namespace

    async def get_item(self, id_: str, **kwargs) -> ReadSchemaType:
        cache_key = self.cache_mask.format(**kwargs, id_=id_)
        item = await self.cache.get(cache_key)
        if item:
            return item
        item = await self.repo.get(id_=id_)  # type: ignore
        await self.cache.add(cache_key, jsonable_encoder(item))
        return item

    async def list_items(self, **kwargs) -> list[ReadSchemaType]:
        namespace = self.cache_namespace.format(**kwargs)
        items = await self.cache.get(namespace)
        if items:
            return items
        items = await self.repo.get_list(**kwargs)
        await self.cache.add(namespace, jsonable_encoder(items))
        return items

    async def create_item(
        self, obj_in: CreateSchemaType, back_task: BackgroundTasks, **kwargs
    ) -> ReadSchemaType:
        item = await self.repo.create(obj_in=obj_in, **kwargs)
        cache_key = self.cache_mask.format(**kwargs, id_=item.id)
        delete_pattern = cache_key.split(':')[0] + '*'
        back_task.add_task(self.cache.multi_clear, delete_pattern, self.cache_root)
        await self.cache.add(cache_key, jsonable_encoder(item))
        return item

    async def update_item(
        self, id_: str, obj_in: UpdateSchemaType, **kwargs
    ) -> ReadSchemaType:
        item = await self.repo.update(id_=id_, obj_in=obj_in)  # type: ignore
        cache_key = self.cache_mask.format(**kwargs, id_=item.id)
        await self.cache.add(cache_key, jsonable_encoder(item))
        await self.cache.clear(self.cache_namespace.format(**kwargs))
        return item

    async def delete_item(
        self, id_: str, back_task: BackgroundTasks, **kwargs
    ) -> JSONResponse:
        item = await self.repo.delete(id_=id_)  # type: ignore
        mask = self.cache_mask.format(**kwargs, id_=id_).split(':')[0] + '*'
        back_task.add_task(self.cache.multi_clear, mask, self.cache_root)
        return item
