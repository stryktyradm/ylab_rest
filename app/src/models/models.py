import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base_class import Base


def generate_uuid():
    return str(uuid.uuid4())


class Menu(Base):
    __tablename__ = 'menu'  # noqa

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, nullable=False, default=generate_uuid
    )
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str | None]

    submenus: Mapped[list['SubMenu']] = relationship(
        back_populates='menu', cascade='all, delete', lazy='selectin'
    )


class SubMenu(Base):
    __tablename__ = 'submenu'  # noqa

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=generate_uuid
    )
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str | None]
    menu_id: Mapped[str] = mapped_column(ForeignKey('menu.id'), nullable=False)

    menu: Mapped['Menu'] = relationship(back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu', cascade='all, delete', lazy='selectin'
    )


class Dish(Base):
    __tablename__ = 'dish'  # noqa

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, nullable=False, default=generate_uuid
    )
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str | None]
    price: Mapped[float]
    submenu_id: Mapped[str] = mapped_column(ForeignKey('submenu.id'), nullable=False)

    submenu: Mapped['SubMenu'] = relationship(back_populates='dishes')
