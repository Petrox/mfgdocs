"""Handles UI element representations"""
import base64
import json

from size_aware_control import SizeAwareControl
import flet as ft
from PIL import Image
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
        self.border_x = None
        self.border_y = None
        self.json_clickable_objects = None
        self.graphviz_json = None
        self.viewport_height = None
        self.viewport_width = None
        self.scale = 1.0
        self.previous_scale = 1.0
        self.zoom_x = None
        self.zoom_y = None
        self.offset_x = 0
        self.offset_y = 0
        self.mfgdocsapp = mfgdocsapp
        self.storage = mfgdocsapp.storage
        self.ctrl = mfgdocsapp.ctrl
        self.image_width = 1
        self.image_height = 1

    def get_overview_dialog(self, file_name='assets/generated/overview.dot'):
        dlg = ft.AlertDialog(visible=True,
                             open=True,
                             modal=False,
                             title=ft.Text('Overview'),
                             on_dismiss=self.clear_overview_image)

        self.image_width, self.image_height = self.get_image_size(file_name)
        self.graphviz_json = self.load_graphviz_json(f'{file_name}.json')
        self.process_graphviz_json(self.graphviz_json)
        self.scale = 1.0
        with open(f'{file_name}.png', mode='rb') as file:
            file_content = file.read()
        image_src = base64.b64encode(file_content).decode('utf-8')
        self.ctrl['overview_image'] = ft.Image(src_base64=image_src, expand=True)
        self.ctrl['overview_image_background'] = ft.Container(height=self.image_height * 2,
                                                              width=self.image_width * 2,
                                                              bgcolor='green',
                                                              content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,
                                                                                controls=[
                                                                                    ft.Row(controls=[
                                                                                        self.ctrl['overview_image']],
                                                                                        alignment=ft.MainAxisAlignment.CENTER)])
                                                              )
        self.ctrl['overview_image_stack'] = ft.Stack(
            controls=[ft.Container(content=self.ctrl['overview_image_background']),
                      ft.GestureDetector(on_pan_update=self.on_pan_update,
                                         on_scroll=self.on_scroll_update,
                                         on_tap_up=self.click_overview_image)],
            left=0, top=0, width=3000, height=3000)
        dlg.content = SizeAwareControl(content=ft.Stack(controls=[self.ctrl['overview_image_stack']]),
                                       on_resize=self.content_resize,
                                       width=2000)
        return dlg

    def reset_image_position(self):
        self.scale = None
        self.update_image_position()

    def update_image_position(self):

        viewport_ratio = self.viewport_width / self.viewport_height
        image_ratio = self.image_width / self.image_height
        # we want to pad the image with a border so that the resulting object has the same ratio as the viewport
        if viewport_ratio > image_ratio:
            # viewport is wider than image, so we pad the image with a border on the left and right
            self.border_x = (self.image_height * viewport_ratio) - self.image_width
            self.border_y = 0
        else:
            self.border_y = (self.image_width / viewport_ratio) - self.image_height
            self.border_x = 0
        minscale = self.viewport_width / (self.image_width + self.border_x)
        if self.scale is None:
            self.scale = minscale
        self.scale = self.clamp(self.scale, minscale, 30)

        stack_width = (self.image_width + self.border_x) * self.scale
        stack_height = (self.image_height + self.border_y) * self.scale
        stack_overflow_x = stack_width - self.viewport_width
        stack_overflow_y = stack_height - self.viewport_height

        if self.scale != self.previous_scale:
            if self.zoom_x is not None and self.ctrl['overview_image_stack'].width is not None:
                prevstack_width = (self.image_width + self.border_x) * self.previous_scale
                prevstack_height = (self.image_height + self.border_y) * self.previous_scale
                size_delta_x = stack_width - prevstack_width
                size_delta_y = stack_height - prevstack_height
                of_x = size_delta_x * (self.zoom_x / self.ctrl['overview_image_stack'].width)
                of_y = size_delta_y * (self.zoom_y / self.ctrl['overview_image_stack'].height)
                self.offset_x -= of_x
                self.offset_y -= of_y
            self.previous_scale = self.scale

        # print(f"borderratio: {(self.image_width + border_x) / (self.image_height + border_y):.2f} == {viewport_ratio:.2f}")
        # print(f"border: {self.image_width}+{border_x} == {self.viewport_width}     and  {self.image_height}+{border_y} == {self.viewport_height}")
        self.offset_x = self.clamp(self.offset_x, -stack_overflow_x, 0)
        self.offset_y = self.clamp(self.offset_y, -stack_overflow_y, 0)
        self.ctrl['overview_image_stack'].width = stack_width
        self.ctrl['overview_image_stack'].height = stack_height
        self.ctrl['overview_image'].width = self.image_width * self.scale
        self.ctrl['overview_image'].height = self.image_height * self.scale
        self.ctrl['overview_image_stack'].left = self.offset_x
        self.ctrl['overview_image_stack'].top = self.offset_y
        self.ctrl['overview_image_stack'].update()

    def content_resize(self, event: ft.canvas.CanvasResizeEvent):
        print(f"content resize: {event.width} {event.height}")
        self.viewport_width = event.width
        self.viewport_height = event.height
        self.reset_image_position()

    def get_image_size(self, file_name: str):
        """Opens the file and returns the image size using PIL"""
        im = Image.open(f'{file_name}.png')
        return im.size

    def load_graphviz_json(self, file_name: str):
        with open(file_name, mode='r') as file:
            file_content = json.load(file)
        return file_content

    def on_pan_update(self, event: ft.DragUpdateEvent):
        print(f"pan update: {self.ctrl['overview_image_stack'].top} {event.delta_x}, {event.delta_y}")
        self.offset_x += event.delta_x
        self.offset_y += event.delta_y
        self.update_image_position()

    def on_scroll_update(self, event: ft.ScrollEvent):

        self.scale = self.scale - event.scroll_delta_y * 0.0001
        self.zoom_x = event.local_x
        self.zoom_y = event.local_y
        print(
            f'scroll update: {self.ctrl['overview_image_stack'].width} {event.scroll_delta_y} {self.scale}')
        self.update_image_position()

    def clear_overview_image(self, e):
        del e
        self.ctrl['overview_image'].src = ''
        self.ctrl['overview_image'] = None

    def clamp(self, value: float, min: float, max: float) -> float:
        if value < min:
            return min
        if value > max:
            return max
        return value

    # https://stackoverflow.com/a/76349368
    def convert_points_to_inches(self, points: float) -> float:
        return points / 72

    def convert_points_to_pixels(self, points: float) -> float:
        return points / 72 * self.json_dpi

    def convert_pixels_to_inches(self, pixels: float) -> float:
        return pixels / self.json_dpi

    def convert_inches_to_pixels(self, inches: float) -> float:
        return inches * self.json_dpi

    def process_graphviz_json(self, json):
        self.json_clickable_objects = {}
        if json is None:
            return
        self.json_dpi = float(json['dpi'])
        self.json_boundingbox = json['bb'].split(',')
        self.json_bb_x1 = self.convert_points_to_pixels(float(self.json_boundingbox[0]))
        self.json_bb_y1 = self.convert_points_to_pixels(float(self.json_boundingbox[1]))
        self.json_bb_x2 = self.convert_points_to_pixels(float(self.json_boundingbox[2]))
        self.json_bb_y2 = self.convert_points_to_pixels(float(self.json_boundingbox[3]))
        self.json_size = json['size'].split(',')
        print(f"json size: {self.json_bb_x1} {self.json_bb_y1} {self.json_bb_x2} {self.json_bb_y2}")
        print(
            f"image size: {self.image_width} {self.image_height} {self.convert_pixels_to_inches(self.image_width)} {self.convert_pixels_to_inches(self.image_height)}")
        self.json_clickable_objects = {}
        for n in json['objects']:
            item = {}
            pos = n['pos'].split(',')
            item['key'] = n['name']
            item['height'] = self.convert_inches_to_pixels(float(n['height']))
            item['width'] = self.convert_inches_to_pixels(float(n['width']))
            item['pos_x'] = self.convert_points_to_pixels(float(pos[0]))
            item['pos_y'] = self.image_height - (self.convert_points_to_pixels(float(pos[1])))
            item['pos_x1'] = item['pos_x'] - item['width'] / 2
            item['pos_y1'] = item['pos_y'] - item['height'] / 2
            item['pos_x2'] = item['pos_x'] + item['width'] / 2
            item['pos_y2'] = item['pos_y'] + item['height'] / 2
            self.json_clickable_objects[n['name']] = item
            print(f"clickable object: {n['name']} {item['pos_x']} {item['pos_y']} {item['width']} {item['height']}")

    def click_overview_image(self, event: ft.ControlEvent):
        print(f"click on overview image: {event.local_x} {event.local_y}")

        # we don't need to handle offset_x and offset_y since the coordinates are relative to the control which has been offset already
        x = (event.local_x)/self.scale-self.border_x/2
        y = (event.local_y)/self.scale-self.border_y/2
        print(f"click on overview image x: {event.local_x} {self.offset_x} {self.scale:.2f} {self.border_x} {x}")
        print(f"click on overview image y: {event.local_y} {self.offset_y} {self.scale:.2f} {self.border_y} {y}")
        if self.json_clickable_objects is None:
            return
        for k, v in self.json_clickable_objects.items():
            if v['pos_x1'] < x < v['pos_x2'] and v['pos_y1'] < y < v['pos_y2']:
                print(f"click on {k}")
                if k.lower().startswith('step'):
                    self.mfgdocsapp.page.dialog.open = False
                    self.mfgdocsapp.load_mainmarkdown_step(k)
                    self.mfgdocsapp.page.update()
                    return
        print('click on nothing')
