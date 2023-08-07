from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src import models, schemas
from src.api.deps import get_menu_id, get_menu_model
from src.service import SubMenuService, get_submenu_service

router = APIRouter()


@router.get('/{submenu_id}', response_model=schemas.SubMenuRead, status_code=status.HTTP_200_OK)
async def get_submenu(
    submenu_id: str,
    service: SubMenuService = Depends(get_submenu_service)
) -> schemas.SubMenuRead:
    response = await service.get_item(id_=submenu_id)
    return response


@router.get('/', response_model=list[schemas.SubMenuRead], status_code=status.HTTP_200_OK)
async def get_submenus(
    menu_id: str = Depends(get_menu_id),
    service: SubMenuService = Depends(get_submenu_service)
) -> list[schemas.SubMenuRead]:
    response = await service.list_items(menu_id=menu_id)
    return response


@router.post('/', response_model=schemas.SubMenuRead, status_code=status.HTTP_201_CREATED)
async def create_submenu(
    item_in: schemas.SubMenuCreate,
    menu: models.Menu = Depends(get_menu_model),
    service: SubMenuService = Depends(get_submenu_service)
) -> schemas.SubMenuRead:
    response = await service.create_item(obj_in=item_in, menu_id=menu.id)
    return response


@router.patch('/{submenu_id}', response_model=schemas.SubMenuRead)
async def update_submenu(
    submenu_id: str,
    item_in: schemas.SubMenuUpdate,
    service: SubMenuService = Depends(get_submenu_service)
) -> schemas.SubMenuRead:
    response = await service.update_item(id_=submenu_id, obj_in=item_in)
    return response


@router.delete('/{submenu_id}')
async def delete_submenu(
    submenu_id: str,
    menu: models.Menu = Depends(get_menu_model),
    service: SubMenuService = Depends(get_submenu_service)
) -> JSONResponse:
    response = await service.delete_item(id_=submenu_id, menu_id=menu.id)
    return response
