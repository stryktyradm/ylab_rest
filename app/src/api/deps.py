from fastapi import Depends, Request
from src import schemas
from src.repository import (
    MenuCRUDRepository,
    SubMenuCRUDRepository,
    get_menu_repository,
    get_submenu_repository,
)


async def get_menu_model(
    request: Request,
    repo: MenuCRUDRepository = Depends(get_menu_repository)
) -> schemas.MenuRead:
    path_id = request.path_params.get('menu_id')
    menu = await repo.get(id_=path_id)
    return menu


async def get_submenu_model(
    request: Request,
    repo: SubMenuCRUDRepository = Depends(get_submenu_repository)
) -> schemas.SubMenuRead:
    path_id = request.path_params.get('submenu_id')
    submenu = await repo.get(id_=path_id)
    return submenu


def get_menu_id(request: Request) -> str:
    return request.path_params.get('menu_id')


def get_submenu_id(request: Request) -> str:
    return request.path_params.get('submenu_id')
