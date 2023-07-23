from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src import crud
from src.api.deps import get_db
from src.schemas import MenuRead, MenuCreate, MenuUpdate

router = APIRouter()


@router.get("/{menu_id}", response_model=MenuRead, status_code=status.HTTP_200_OK)
def get_menu(menu_id: int, db: Session = Depends(get_db)) -> MenuRead:
    response = crud.menu.get(db=db, id_=menu_id)
    return response


@router.get("/", response_model=list[MenuRead], status_code=status.HTTP_200_OK)
def get_menus(db: Session = Depends(get_db)) -> list[MenuRead]:
    response = crud.menu.get_list(db=db)
    return response


@router.post("/", response_model=MenuRead, status_code=status.HTTP_201_CREATED)
def create_menu(
    item_in: MenuCreate,
    db: Session = Depends(get_db)
) -> MenuRead:
    response = crud.menu.create(db=db, obj_in=item_in)
    return response


@router.patch("/{menu_id}", response_model=MenuRead)
def update_menu(
    menu_id: int,
    item_in: MenuUpdate,
    db: Session = Depends(get_db)
) -> MenuRead:
    response = crud.menu.update(db=db, id_=menu_id, obj_in=item_in)
    return response


@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    response = crud.menu.delete(db=db, id_=menu_id)
    return response
