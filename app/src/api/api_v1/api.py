from fastapi import APIRouter

from src.api.api_v1.endpoints import menu, submenu, dish

api_router = APIRouter()

api_router.include_router(
    menu.router,
    prefix="/menus",
    tags=["Menus"]
)
api_router.include_router(
    submenu.router,
    prefix="/menus/{menu_id}/submenus",
    tags=["Submenus"]
)
api_router.include_router(
    dish.router,
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"]
)
