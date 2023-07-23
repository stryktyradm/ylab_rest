from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src import crud
from src.schemas import DishCreate, DishRead, DishUpdate
from src.api.deps import get_db, get_submenu_model, get_submenu_id
from src.models import SubMenu

router = APIRouter()


@router.get("/{dish_id}", response_model=DishRead, status_code=status.HTTP_200_OK)
def get_dish(dish_id: int, db: Session = Depends(get_db)) -> DishRead:
    response = crud.dish.get(db=db, id_=dish_id)
    return response


@router.get("/", response_model=list[DishRead], status_code=status.HTTP_200_OK)
def get_dishes(
    db: Session = Depends(get_db),
    submenu_id: int = Depends(get_submenu_id)
) -> list[DishRead]:
    response = crud.dish.get_list(db=db, submenu_id=submenu_id)
    return response


@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
def create_dish(
    item_in: DishCreate,
    db: Session = Depends(get_db),
    submenu_model: SubMenu = Depends(get_submenu_model)
) -> DishRead:
    response = crud.dish.create(db=db, obj_in=item_in, submenu_id=submenu_model.id)
    return response


@router.patch("/{dish_id}", response_model=DishRead)
def update_dish(
    dish_id: int,
    item_in: DishUpdate,
    db: Session = Depends(get_db)
) -> DishRead:
    response = crud.dish.update(db=db, id_=dish_id, obj_in=item_in)
    return response


@router.delete("/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    response = crud.dish.delete(db=db, id_=dish_id)
    return response
