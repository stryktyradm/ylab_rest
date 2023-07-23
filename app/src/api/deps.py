from typing import Generator, Any

from sqlalchemy.orm import Session
from fastapi import Request, Depends

from src.db.session import SessionLocal
from src import crud
from src.models import Menu, SubMenu


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_menu_model(request: Request, db: Session = Depends(get_db)) -> Menu:
    path_id = request.path_params.get("menu_id")
    model = crud.menu.get(db=db, id_=path_id, in_db=True)
    return model


def get_submenu_model(request: Request, db: Session = Depends(get_db)) -> SubMenu:
    path_id = request.path_params.get("submenu_id")
    model = crud.submenu.get(db=db, id_=path_id, in_db=True)
    return model


def get_menu_id(request: Request) -> Any:
    return request.path_params.get("menu_id")


def get_submenu_id(request: Request) -> Any:
    return request.path_params.get("submenu_id")

