from typing import Optional, List

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.db.base_class import Base


class Menu(Base):
    __tablename__ = 'menu' # noqa

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[Optional[str]]

    submenus: Mapped[List["SubMenu"]] = relationship(
        back_populates="menu", cascade='all, delete', lazy='joined'
    )


class SubMenu(Base):
    __tablename__ = 'submenu' # noqa

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[Optional[str]]
    menu_id: Mapped[int] = mapped_column(ForeignKey('menu.id'), nullable=False)

    menu: Mapped["Menu"] = relationship(back_populates="submenus")
    dishes: Mapped[List["Dish"]] = relationship(
        back_populates="submenu", cascade='all, delete', lazy="joined"
    )


class Dish(Base):
    __tablename__ = 'dish' # noqa

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[Optional[str]]
    price: Mapped[float]
    submenu_id: Mapped[int] = mapped_column(ForeignKey('submenu.id'), nullable=False)

    submenu: Mapped["SubMenu"] = relationship(back_populates="dishes")
