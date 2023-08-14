import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from src import models
from src.admin.parse_menu_xlsx import from_xlsx_to_dict


async def init_db(session: AsyncSession):
    all_menus = from_xlsx_to_dict()
    for menu_data in all_menus:
        menu = models.Menu(
            id=uuid.UUID(menu_data['id']),
            title=menu_data['title'],
            description=menu_data['description'],
        )
        session.add(menu)
        for submenu_data in menu_data['submenus']:
            submenu = models.SubMenu(
                id=uuid.UUID(submenu_data['id']),
                title=submenu_data['title'],
                description=submenu_data['description'],
                menu_id=menu.id
            )
            session.add(submenu)
            for dish_data in submenu_data['dishes']:
                dish = models.Dish(
                    id=uuid.UUID(dish_data['id']),
                    title=dish_data['title'],
                    description=dish_data['description'],
                    price=dish_data['price'],
                    submenu_id=submenu.id
                )
                session.add(dish)
    await session.commit()
