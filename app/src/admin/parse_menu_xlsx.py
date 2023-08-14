import openpyxl


def from_xlsx_to_dict(path: str = 'src/admin/Menu.xlsx') -> list:
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    menus: list = []
    menu_count = 0

    for row in ws.iter_rows():
        if row[0].value is None:
            submenu_count = 0
            if row[1].value is None:
                id_, title, description, price = row[2].value, row[3].value, row[4].value, row[5].value
                dish = {'id': id_, 'title': title, 'description': description, 'price': price}
                menus[menu_count - 1]['submenus'][submenu_count - 1]['dishes'].append(dish)
                continue
            id_, title, description = row[1].value, row[2].value, row[3].value
            submenu = {'id': id_, 'title': title, 'description': description, 'dishes': []}
            menus[menu_count - 1]['submenus'].append(submenu)
            submenu_count += 1
            continue
        id_, title, description = row[0].value, row[1].value, row[2].value
        menu = {'id': id_, 'title': title, 'description': description, 'submenus': []}
        menus.append(menu)
        menu_count += 1

    return menus


if __name__ == '__main__':
    from_xlsx_to_dict()
