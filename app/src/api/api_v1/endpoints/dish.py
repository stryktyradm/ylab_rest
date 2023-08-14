from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from src import models, schemas
from src.api.deps import get_menu_id, get_menu_model, get_submenu_id, get_submenu_model
from src.service import DishService, get_dish_service

router = APIRouter()


@router.get('/{dish_id}', response_model=schemas.DishRead, status_code=status.HTTP_200_OK)
async def get_dish(
    dish_id: str,
    menu_id: str = Depends(get_menu_id),
    submenu_id: str = Depends(get_submenu_id),
    service: DishService = Depends(get_dish_service)
) -> schemas.DishRead:
    response = await service.get_item(
        id_=dish_id, menu_id=menu_id, submenu_id=submenu_id
    )
    return response


@router.get('/', response_model=list[schemas.DishRead], status_code=status.HTTP_200_OK)
async def get_dishes(
    menu_id: str = Depends(get_menu_id),
    submenu_id: str = Depends(get_submenu_id),
    service: DishService = Depends(get_dish_service)
) -> list[schemas.DishRead]:
    response = await service.list_items(menu_id=menu_id, submenu_id=submenu_id)
    return response


@router.post('/', response_model=schemas.DishRead, status_code=status.HTTP_201_CREATED)
async def create_dish(
    item_in: schemas.DishCreate,
    background_task: BackgroundTasks,
    menu: models.Menu = Depends(get_menu_model),
    submenu: models.SubMenu = Depends(get_submenu_model),
    service: DishService = Depends(get_dish_service)
) -> schemas.DishRead:
    response = await service.create_item(
        obj_in=item_in, back_task=background_task, menu_id=menu.id, submenu_id=submenu.id
    )
    return response


@router.patch('/{dish_id}', response_model=schemas.DishRead)
async def update_dish(
    dish_id: str,
    item_in: schemas.DishUpdate,
    menu_id: str = Depends(get_menu_id),
    submenu_id: str = Depends(get_submenu_id),
    service: DishService = Depends(get_dish_service)
) -> schemas.DishRead:
    response = await service.update_item(
        id_=dish_id, obj_in=item_in, menu_id=menu_id, submenu_id=submenu_id
    )
    return response


@router.delete('/{dish_id}')
async def delete_dish(
    dish_id: str,
    background_task: BackgroundTasks,
    menu: models.Menu = Depends(get_menu_model),
    submenu: models.SubMenu = Depends(get_submenu_model),
    service: DishService = Depends(get_dish_service)
) -> JSONResponse:
    response = await service.delete_item(
        id_=dish_id, back_task=background_task, menu_id=menu.id, submenu_id=submenu.id
    )
    return response
