"""Handles UI element representations"""
import flet as ft
from model import Part, Step, Resource  # Location, Machine, Consumable, Role, Tool, Action


class Frontend:
    """Handles the UI elements of the objects in storage.
    """
    def __init__(self, mfgdocsapp):
        self.mfgdocsapp = mfgdocsapp

    def get_searchresultitem_part(self, pk: int) -> ft.Control:
        item: Part = self.mfgdocsapp.storage.cache_parts.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.LIGHT_GREEN_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MOTORCYCLE),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_step(self, pk: int) -> ft.Control:
        item: Step = self.mfgdocsapp.storage.cache_steps.data[pk]
        c = ft.Container()
        c.key=item.key
        c.bgcolor = ft.colors.LIGHT_BLUE_400
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.BUILD),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_location(self, pk: int) -> ft.Control:
        item: Resource = self.mfgdocsapp.storage.cache_locations.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.BROWN_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.LOCATION_PIN),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_action(self, pk: int) -> ft.Control:
        item: Resource = self.mfgdocsapp.storage.cache_actions.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.CYAN_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.WORK),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_tool(self, pk: int) -> ft.Control:
        item: Resource = self.mfgdocsapp.storage.cache_tools.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.ORANGE_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.CHAIR),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_machine(self, pk: int) -> ft.Control:
        item: Resource = self.mfgdocsapp.storage.cache_tools.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.INDIGO_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MICROWAVE),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_consumable(self, pk: int) -> ft.Control:
        item: Resource = self.mfgdocsapp.storage.cache_consumables.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.GREY_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.WATER_DROP),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_role(self, pk: int) -> ft.Control:
        item: Resource = self.mfgdocsapp.storage.cache_roles.data[pk]
        c = ft.Container()
        c.bgcolor = ft.colors.TEAL_100
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MAN),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c
