"""Handles UI element representations"""
import base64

import flet as ft
from model import Part, Step, Action, Tool, Machine, Consumable, Role


class Frontend:
    """Handles the UI elements of the objects in storage.
    """
    singleton_frontend = None

    def __init__(self, mfgdocsapp):
        self.mfgdocsapp = mfgdocsapp
        Frontend.singleton_frontend = self

    def get_searchresultitem(self, obj, key: str = None) -> ft.Control:
        item_type = obj.__class__.__name__.lower()

        if hasattr(self, f'get_searchresultitem_{item_type}'):
            return getattr(self, f'get_searchresultitem_{item_type}')(item=obj, key=key)

        return ft.Text(f'frontend.get_searchresultitem(): Unknown object type {item_type} {obj}')

    def get_searchresultitem_part(self, item: Part or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Part = self.mfgdocsapp.storage.cache_parts.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.LIGHT_GREEN_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MOTORCYCLE),
                                     ft.Text(key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_step(self, item: Part or int or str, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Step = self.mfgdocsapp.storage.cache_steps.data[item]
        if isinstance(item, str):
            item: Step = self.mfgdocsapp.storage.cache_steps.get_by_unique_key('key', item)
        c = ft.Container()
        c.key = item.key
        c.bgcolor = ft.colors.LIGHT_BLUE_400
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.BUILD),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_location(self, item: Step or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Step = self.mfgdocsapp.storage.cache_locations.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.BROWN_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.LOCATION_PIN),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_action(self, item: Action or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Action = self.mfgdocsapp.storage.cache_actions.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.CYAN_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.WORK),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_tool(self, item: Tool or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Tool = self.mfgdocsapp.storage.cache_tools.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.ORANGE_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.CHAIR),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_machine(self, item: Machine or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Machine = self.mfgdocsapp.storage.cache_machines.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.INDIGO_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MICROWAVE),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_consumable(self, item: Consumable or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Consumable = self.mfgdocsapp.storage.cache_consumables.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.GREY_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.WATER_DROP),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c

    def get_searchresultitem_role(self, item: Role or int, key: str = None) -> ft.Control:
        if isinstance(item, int):
            item: Role = self.mfgdocsapp.storage.cache_roles.data[item]
        c = ft.Container()
        c.bgcolor = ft.colors.TEAL_600
        c.border = ft.RoundedRectangleBorder()
        c.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.MAN),
                                     ft.Text(item.key, color='white'), ft.Text(item.name, color='white')])
        return c


class Overview:

    def __init__(self, mfgdocsapp: 'MFGDocsApp'):
        self.mfgdocsapp = mfgdocsapp
        self.storage = mfgdocsapp.storage
        self.ctrl = mfgdocsapp.ctrl

    def get_overview_dialog(self, file_name='assets/generated/overview.dot.png'):
        dlg = ft.AlertDialog(visible=True,
                             open=True,
                             modal=False,
                             title=ft.Text('Overview'),
                             on_dismiss=self.clear_overview_image)
        with open(file_name, mode='rb') as file:
            file_content = file.read()
        image_src = base64.b64encode(file_content).decode('utf-8')
        self.ctrl['overview_image'] = ft.Image(src_base64=image_src, expand=True)
        self.ctrl['overview_image_stack'] = ft.Stack(
            controls=[ft.Column([self.ctrl['overview_image']]),
                      ft.GestureDetector(on_pan_update=self.on_pan_update,on_scroll=self.on_scroll_update)],
            left=0, top=0, width=3000, height=3000)
        dlg.content = ft.Container(content=ft.Stack(controls=[self.ctrl['overview_image_stack']],
                                                    width=3000,
                                                    height=3000))
        return dlg

    def on_pan_update(self, event: ft.DragUpdateEvent):
        print(f"pan update: {self.ctrl['overview_image_stack'].top} {event.delta_x}, {event.delta_y}")
        self.ctrl['overview_image_stack'].top += event.delta_y
        self.ctrl['overview_image_stack'].left += event.delta_x
        self.ctrl['overview_image_stack'].update()

    def on_scroll_update(self, event: ft.ScrollEvent):
        print(f'scroll update: {self.ctrl['overview_image_stack'].width} {event.scroll_delta_y}, {event.scroll_delta_y}')
        self.ctrl['overview_image_stack'].top -= event.scroll_delta_y/2
        self.ctrl['overview_image_stack'].left -= event.scroll_delta_y/2
        self.ctrl['overview_image_stack'].width += event.scroll_delta_y
        self.ctrl['overview_image_stack'].height += event.scroll_delta_y
        self.ctrl['overview_image_stack'].update()

    def clear_overview_image(self, e):
        del e
        self.ctrl['overview_image'].src = ''
        self.ctrl['overview_image'] = None
