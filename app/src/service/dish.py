from typing import TypeVar

from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from src.repository.dish import DishCRUDRepository
from src.schemas.dish import DishCreate, DishRead, DishUpdate
from src.service.base import BaseService

DishRepository = TypeVar('DishRepository', bound=DishCRUDRepository)


class DishService(BaseService[DishRepository, DishCreate, DishRead, DishUpdate]):
    async def list_items(self, **kwargs) -> list[DishRead]:
        namespace = self.cache_namespace.format(**kwargs)
        items = await self.cache.get(namespace)
        if items:
            return items
        items = await self.repo.get_list(submenu_id=kwargs.get('submenu_id'))  # type: ignore
        await self.cache.add(namespace, jsonable_encoder(items))
        return items

    async def create_item(
        self, obj_in: DishCreate, back_task: BackgroundTasks, **kwargs
    ) -> DishRead:
        item = await self.repo.create(obj_in=obj_in, submenu_id=kwargs.get('submenu_id'))  # type: ignore
        mask = self.cache_mask.format(**kwargs, id_=item.id)
        delete_pattern = mask.split(':')[0] + '*'
        back_task.add_task(self.cache.multi_clear, delete_pattern, self.cache_root)
        await self.cache.add(mask, jsonable_encoder(item))
        return item
