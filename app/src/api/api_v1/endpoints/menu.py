from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from src import schemas
from src.service import MenuService, get_menu_service

router = APIRouter()


@router.get('/all_menus', response_model=list[schemas.NestedMenu], status_code=status.HTTP_200_OK)
async def get_all_menus(
    service: MenuService = Depends(get_menu_service)
) -> list[schemas.NestedMenu] | Any:
    response = await service.get_all_items()
    return response


@router.get('/{menu_id}', response_model=schemas.MenuRead, status_code=status.HTTP_200_OK)
async def get_menu(
    menu_id: str,
    service: MenuService = Depends(get_menu_service)
) -> schemas.MenuRead:
    response = await service.get_item(id_=menu_id)
    return response


@router.get('/', response_model=list[schemas.MenuRead], status_code=status.HTTP_200_OK)
async def get_menus(
    service: MenuService = Depends(get_menu_service)
) -> list[schemas.MenuRead]:
    response = await service.list_items()
    return response


@router.post('/', response_model=schemas.MenuRead, status_code=status.HTTP_201_CREATED)
async def create_menu(
    item_in: schemas.MenuCreate,
    background_task: BackgroundTasks,
    service: MenuService = Depends(get_menu_service)
) -> schemas.MenuRead:
    response = await service.create_item(obj_in=item_in, back_task=background_task)
    return response


@router.patch('/{menu_id}', response_model=schemas.MenuRead)
async def update_menu(
    menu_id: str,
    item_in: schemas.MenuUpdate,
    service: MenuService = Depends(get_menu_service)
) -> schemas.MenuRead:
    response = await service.update_item(id_=menu_id, obj_in=item_in)
    return response


@router.delete('/{menu_id}')
async def delete_menu(
    menu_id: str,
    background_tasks: BackgroundTasks,
    service: MenuService = Depends(get_menu_service)
) -> JSONResponse:
    response = await service.delete_item(id_=menu_id, back_task=background_tasks)
    return response
