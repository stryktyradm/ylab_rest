from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import crud
from src.api.deps import get_db, get_menu_model, get_menu_id
from src.models import Menu
from src.schemas import SubMenuCreate, SubMenuRead, SubMenuUpdate

router = APIRouter()


@router.get("/{submenu_id}", response_model=SubMenuRead, status_code=status.HTTP_200_OK)
def get_submenu(submenu_id: int, db: Session = Depends(get_db)) -> SubMenuRead:
    response = crud.submenu.get(db=db, id_=submenu_id)
    return response


@router.get("/", response_model=list[SubMenuRead], status_code=status.HTTP_200_OK)
def get_submenus(
    db: Session = Depends(get_db),
    menu_id: int = Depends(get_menu_id)
) -> list[SubMenuRead]:
    response = crud.submenu.get_list(db=db, menu_id=menu_id)
    return response


@router.post("/", response_model=SubMenuRead, status_code=status.HTTP_201_CREATED)
def create_submenu(
    item_in: SubMenuCreate,
    db: Session = Depends(get_db),
    menu_model: Menu = Depends(get_menu_model)
) -> SubMenuRead:
    response = crud.submenu.create(db=db, obj_in=item_in, menu_id=menu_model.id)
    return response


@router.patch("/{submenu_id}", response_model=SubMenuRead)
def update_submenu(
    submenu_id: int,
    item_id: SubMenuUpdate,
    db: Session = Depends(get_db)
) -> SubMenuRead:
    response = crud.submenu.update(db=db, id_=submenu_id, obj_in=item_id)
    return response


@router.delete("/{submenu_id}")
def delete_submenu(submenu_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    response = crud.submenu.delete(db=db, id_=submenu_id)
    return response
