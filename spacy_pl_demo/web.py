from typing import NamedTuple, List


class MenuItem(NamedTuple):
    name: str
    href: str
    active: bool


DEFAULT_MENU_ITEMS = [
    # MenuItem('Home', '/', False),
    MenuItem('Lemmatizer', '/lemmatizer', False),
]


def menu_for_page(
        active_page_name: str='Home',
        menu_items: List[MenuItem]=DEFAULT_MENU_ITEMS
) -> List[MenuItem]:
    print("generating menu...")
    print(menu_items)
    return [_decide_active(item, active_page_name) for item in menu_items]


def _decide_active(menu_item: MenuItem, active_page_name: str) -> MenuItem:
    processed_item = MenuItem(
        name=menu_item.name,
        href=menu_item.href,
        active=(menu_item.name == active_page_name)
    )
    print(f"item: {repr(processed_item)}")
    return processed_item
