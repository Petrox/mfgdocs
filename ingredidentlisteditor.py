"""
A user control to edit a list of resources and their quantities.
"""
import flet as ft


class IngredientListEditor(ft.UserControl):
    """Item list and quantity editor."""
    def __init__(self, label, items=None, color=ft.colors.ON_PRIMARY):
        super().__init__()
        if items is None:
            items = {}
        self.color = color
        self.label = label
        self.items = items
        self.controls = []
        self.item_type = None

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
            item_ctrl = ft.Row(data={'key': k, 'value': v},
                               controls=[ft.TextField(label='Amount',
                                                      value=v,
                                                      icon=ft.icons.SHOPPING_CART,
                                                      data={'key': k, 'value': v},
                                                      on_change=self.set_amount),
                                         ft.Text(' x ', style=ft.TextThemeStyle.LABEL_SMALL),
                                         ft.Text(k, style=ft.TextThemeStyle.LABEL_LARGE),
                                         ft.IconButton(icon=ft.icons.DELETE, data={'key': k, 'value': v},
                                                       on_click=self.click_remove)])
            self.controls.append(item_ctrl)
        self.maincontrol = ft.Column(expand=True, controls=self.controls)
        return self.maincontrol
