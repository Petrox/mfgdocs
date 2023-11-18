"""
A user control to edit a list of resources and their quantities.
"""
import flet as ft
from frontend import Frontend
from storage import Storage


class IngredientListEditor(ft.UserControl):
    """Item list and quantity editor."""

    def __init__(self, label, items=None, color=ft.colors.ON_PRIMARY, resource_type=None, storage:Storage=None):
        super().__init__()
        self.storage = storage
        if items is None:
            items = {}
        self.color = color
        self.label = label
        self.items = items
        self.controls = []
        self.resource_type = resource_type

    def get_searchitem(self, obj) -> ft.Control:
        if Frontend.singleton_frontend is None:
            return ft.Text('Frontend.singleton_frontend is None')
        if obj is None:
            return ft.Text('get_searchitem(None)')
        print(f'get_searchitem({obj})')
        return Frontend.singleton_frontend.get_searchresultitem(obj)

    def click_remove(self, event):
        key = event.control.data['key']
        self.remove_maincontrol_by_key(key)
        del self.items[key]
        self.maincontrol.update()

    def remove_maincontrol_by_key(self, key):
        found = None
        for idx, control in enumerate(self.maincontrol.controls):
            if isinstance(control.data, dict) and 'key' in control.data and control.data['key'] == key:
                found = idx
                break
        if found is not None:
            self.maincontrol.controls.pop(found)

    def set_amount(self, event):
        key = event.control.data['key']
        self.items[key] = event.control.value
        self.maincontrol.update()

    def build(self):
        self.controls = [ft.Text(self.label, color=self.color, style=ft.TextThemeStyle.LABEL_LARGE)]
        for k, v in self.items.items():
            item = self.storage.get_resource_by_type_and_key(res_type=self.resource_type, key=k)
            searchitem = self.get_searchitem(item)
            if searchitem is None:
                searchitem = ft.Text(f'Unknown: {k}', style=ft.TextThemeStyle.LABEL_LARGE, selectable=True)
            item_ctrl = ft.Row(data={'key': k, 'value': v},
                               controls=[ft.TextField(label='Amount',
                                                      value=v,
                                                      dense=True,
                                                      text_align=ft.TextAlign.RIGHT,
                                                      icon=ft.icons.SHOPPING_CART,
                                                      data={'key': k, 'value': v},
                                                      on_change=self.set_amount),
                                         ft.Text(' x ', style=ft.TextThemeStyle.LABEL_SMALL),
                                         searchitem,
                                         # ft.Text(k, style=ft.TextThemeStyle.LABEL_LARGE,selectable=True),
                                         ft.IconButton(icon=ft.icons.DELETE, data={'key': k, 'value': v},
                                                       on_click=self.click_remove)])
            self.controls.append(item_ctrl)
        self.maincontrol = ft.Column(expand=True, controls=self.controls)
        return self.maincontrol
