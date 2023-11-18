"""Handles UI element representations"""
import flet as ft
from model import Part, Step,  Action, Tool, Machine, Consumable, Role

class Frontend:
    """Handles the UI elements of the objects in storage.
    """
    singleton_frontend = None
    def __init__(self, mfgdocsapp):
        self.mfgdocsapp = mfgdocsapp
        Frontend.singleton_frontend = self

    def get_searchresultitem(self, obj) -> ft.Control:
        item_type = obj.__class__.__name__.lower()

        if hasattr(self, f'get_searchresultitem_{item_type}'):
            return getattr(self, f'get_searchresultitem_{item_type}')(item=obj)

        return ft.Text(f'frontend.get_searchresultitem(): Unknown object type {item_type} {obj}')

    def get_searchresultitem_part(self, item: Part or int) -> ft.Control:
        if isinstance(item, int):
            item: Part = self.mfgdocsapp.storage.cache_parts.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.LIGHT_GREEN_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MOTORCYCLE),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_step(self, item: Part or int) -> ft.Control:
        if isinstance(item, int):
            item: Step = self.mfgdocsapp.storage.cache_steps.data[item]
        c = ft.Container()
        c.key = item.key
        c.bgcolor = ft.colors.LIGHT_BLUE_400
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.BUILD),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_location(self, item: Step or int) -> ft.Control:
        if isinstance(item, int):
            item: Step = self.mfgdocsapp.storage.cache_locations.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.BROWN_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.LOCATION_PIN),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c


    def get_searchresultitem_action(self, item: Action or int) -> ft.Control:
        if isinstance(item, int):
            item: Action = self.mfgdocsapp.storage.cache_actions.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.CYAN_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.WORK),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_tool(self, item: Tool or int) -> ft.Control:
        if isinstance(item, int):
            item: Tool = self.mfgdocsapp.storage.cache_tools.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.ORANGE_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.CHAIR),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_machine(self, item: Machine or int) -> ft.Control:
        if isinstance(item, int):
            item: Machine = self.mfgdocsapp.storage.cache_machines.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.INDIGO_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MICROWAVE),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_consumable(self, item: Consumable or int) -> ft.Control:
        if isinstance(item, int):
            item: Consumable = self.mfgdocsapp.storage.cache_consumables.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.GREY_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.WATER_DROP),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_role(self, item: Role or int) -> ft.Control:
        if isinstance(item, int):
            item: Role = self.mfgdocsapp.storage.cache_roles.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.TEAL_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MAN),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c
