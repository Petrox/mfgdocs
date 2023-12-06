"""
A user control to edit a list of resources and their quantities.
"""
import flet as ft
from frontend import Frontend
from model import Resource, Step, Part
from storage import Storage


class IngredientListEditor(ft.UserControl):
    """Item list and quantity editor."""

    def __init__(self, label, items=None, color=ft.colors.ON_PRIMARY, resource_type=None, storage: Storage = None,
                 is_inputpart: bool = False):
        super().__init__()
        self.drop = None
        self.is_inputpart = is_inputpart
        self.maincontrol = None
        self.amount = None
        self.storage = storage
        if items is None:
            items = {}
        self.color = color
        self.label = label
        self.items = items
        self.controls = []
        self.resource_type = resource_type

    def get_searchitem(self, obj, key: str = None) -> ft.Control:
        """This method is used to get a search result control for a specific object."""
        if Frontend.singleton_frontend is None:
            return ft.Text('Frontend.singleton_frontend is None')
        if obj is None:
            return ft.Text('get_searchitem(None)')
        print(f'get_searchitem({obj})')
        return Frontend.singleton_frontend.get_searchresultitem(obj, key=key)

    def click_remove(self, event):
        """
        This method is used to remove a specific item from the list.

        Parameters:
        event (ft.Event): The event object that triggered this method. The event object's control data
                          should contain the key of the item to be removed.

        The method does the following:
        1. Retrieves the key of the item from the event's control data.
        2. Calls the `remove_maincontrol_by_key` method to remove the item's control from the main control.
        3. Deletes the item from the `items` dictionary using the retrieved key.
        4. Calls the `update` method of `maincontrol` to reflect the changes in the UI.
        """
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
        """
        This method is used to set the amount of a specific item in the list.

        """
        key = event.control.data['key']
        value = self.int_or_float_from_string(event.control.value)
        event.control.value = str(value)
        self.items[key] = value
        self.maincontrol.update()

    def build(self):
        """This method is used to build the user interface for the ingredient list editor.

        """

        self.controls = [ft.Text(self.label, color=self.color, style=ft.TextThemeStyle.LABEL_LARGE)]
        for k, v in self.items.items():
            item = self.storage.get_resource_by_type_and_key(res_type=self.resource_type, key=k)
            search_item = self.get_searchitem(item, k)
            if search_item is None:
                search_item = ft.Text(f'Unknown: {k}', style=ft.TextThemeStyle.LABEL_LARGE, selectable=True)
            item_ctrl = ft.Row(data={'key': k, 'value': v},
                               controls=[ft.TextField(label='Amount',
                                                      value=v,
                                                      dense=True,
                                                      text_align=ft.TextAlign.RIGHT,
                                                      icon=ft.icons.SHOPPING_CART,
                                                      data={'key': k, 'value': v},
                                                      on_submit=self.set_amount,
                                                      on_blur=self.set_amount),
                                         ft.Text(' x ', style=ft.TextThemeStyle.LABEL_SMALL),
                                         search_item,
                                         # ft.Text(k, style=ft.TextThemeStyle.LABEL_LARGE,selectable=True),
                                         ft.IconButton(icon=ft.icons.DELETE, data={'key': k, 'value': v},
                                                       on_click=self.click_remove)])
            self.controls.append(item_ctrl)

        self.controls.append(ft.Divider())
        self.controls.append(ft.Text('Add Item', color='white', style=ft.TextThemeStyle.HEADLINE_MEDIUM))
        self.amount = ft.TextField(label='Amount',
                                   dense=True,
                                   text_align=ft.TextAlign.RIGHT,
                                   on_blur=self.update_add_button,
                                   on_submit=self.update_add_button,
                                   value='1',
                                   icon=ft.icons.NUMBERS)
        self.drop = ft.Dropdown(label='Item', dense=True, value=None, options=[],
                                on_change=self.update_add_button)
        search = ft.TextField(label='Search',
                              dense=True,
                              on_submit=self.search_change)
        searchbutton = ft.IconButton(icon=ft.icons.SEARCH, on_click=self.search_change)
        search.data = {'searchfield': search, 'dropdown': self.drop}
        searchbutton.data = {'searchfield': search, 'dropdown': self.drop}
        self.addbutton = ft.ElevatedButton(icon=ft.icons.ADD, text="Add Item", on_click=self.click_add, disabled=True)
        r = ft.Column(controls=[self.amount,
                                ft.Row(controls=[search, searchbutton]),
                                self.drop,
                                self.addbutton])
        self.controls.append(r)
        if self.maincontrol is None:
            self.maincontrol = ft.Column(expand=True, controls=self.controls)
        else:
            self.maincontrol.controls = self.controls
        return self.maincontrol

    def search_change(self, event):
        """This method is used to update the dropdown list of items when the search text changes."""

        search = event.control.data['searchfield']
        drop = event.control.data['dropdown']
        txt = search.value
        results = self.find_items(self.storage.cache_by_resource_type(self.resource_type).data, txt)
        drop.options = []
        for r in results:
            if r['key'] not in self.items:
                drop.options.append(ft.dropdown.Option(r['key'], r['key'] + ' - ' + r['value']))

        if self.is_inputpart:
            stepx: Step
            for stepx in self.storage.cache_steps.data.values():
                if stepx.outputparts is not None:
                    for partkey in stepx.outputparts.keys():
                        partx: Part = self.storage.cache_parts.get_by_unique_key('key', partkey)
                        if partx.contains(txt):
                            drop.options.append(ft.dropdown.Option(partx.key + '(' + stepx.key + ')',
                                                                   partx.key + '(' + stepx.key + ') - ' + partx.name))
        drop.update()
        self.update_add_button()
        self.maincontrol.update()

    def update_add_button(self, event=None):
        """This method is used to update the visibility of the add button when the amount
         or the selected item changes.

         """
        del event
        if self.addbutton is None:
            return
        value = self.int_or_float_from_string(self.amount.value)
        if self.amount is None or self.drop is None:
            self.addbutton.disabled = True
        elif len(self.drop.options) == 0:
            self.addbutton.disabled = True
        elif self.drop.value is None:
            self.addbutton.disabled = True
        elif value <= 0:
            self.addbutton.disabled = True
        else:
            self.addbutton.disabled = False
        self.amount.value = str(value)
        self.amount.update()
        self.addbutton.update()

    def int_or_float_from_string(self, s: str) -> int or float:
        """Converts a string to float or int, whichever is appropriate."""
        s = s.strip()
        try:
            v = float(s)
            if v.is_integer():
                return int(v)
            return v
        except ValueError:
            return 0

    def click_add(self, event):
        """This method is used to add an item to the list."""
        del event
        self.items[self.drop.value] = self.int_or_float_from_string(self.amount.value)
        self.build()
        self.maincontrol.update()

    def find_items(self, items, txt):
        """This method is used to find items in the items list that match the search text."""
        results = []
        v: Resource
        k: str
        for k, v in items.items():
            if v.contains(txt):
                results.append({'key': k, 'value': v.name})
        return results
