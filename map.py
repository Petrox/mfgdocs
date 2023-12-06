import base64
import json
import flet as ft
from PIL import Image
from panzoom import PanZoom


class Map:
    """Builds and handles the overview map.


    """
    def __init__(self, mfgdocsapp: 'MFGDocsApp', storage: 'Storage'):
        self.json_size = None
        self.json_bb_x1 = None
        self.json_bb_x2 = None
        self.json_bb_y1 = None
        self.json_bb_y2 = None
        self.json_clickable_objects = None
        self.json_boundingbox = None
        self.json_dpi = None
        self.graphviz_json = None
        self.mapimage_height = None
        self.mapimage_width = None
        self.mfgdocsapp = mfgdocsapp
        self.storage = storage
        self.ctrl = {}
        self.img = ft.Image()
        self.panzoom = PanZoom(self.img, 200, 200, width=1000, height=1000, padding_color='pink')
        self.maincontrol = ft.Container()
        self.ctrl['maincontrol'] = self.maincontrol

    def build(self):
        self.ctrl['map_canvas'] = ft.Text('asd')
        self.ctrl['map_display'] = ft.Column(
            controls=[self.ctrl['map_canvas']]
        )
        self.ctrl['maincontrol'].content = ft.Stack(controls=[self.ctrl['map_display']])
        return self.maincontrol

    def get_image_size(self, file_name: str):
        """Opens the file and returns the image size using PIL"""
        im = Image.open(file_name)
        return im.size

    def load_graphviz_json(self, file_name: str):
        with open(file_name, mode='r') as file:
            file_content = json.load(file)
        return file_content

    def display_map(self, width: int, height: int, file_name: str = 'assets/generated/overview.dot'):
        self.mapimage_width, self.mapimage_height = self.get_image_size(file_name + '.png')
        self.graphviz_json = self.load_graphviz_json(f'{file_name}.json')
        self.parse_graphviz_json(self.graphviz_json)
        with open(f'{file_name}.png', mode='rb') as file:
            file_content = file.read()

        image_src = base64.b64encode(file_content).decode('utf-8')
        self.img = ft.Image(src_base64=image_src, expand=True)
        return PanZoom(
            self.img, self.mapimage_width, self.mapimage_height, width=width, height=height, padding_color='pink'
            )

    # https://stackoverflow.com/a/76349368
    def convert_points_to_inches(self, points: float) -> float:
        return points / 72

    def convert_points_to_pixels(self, points: float) -> float:
        return points / 72 * self.json_dpi

    def convert_pixels_to_inches(self, pixels: float) -> float:
        return pixels / self.json_dpi

    def convert_inches_to_pixels(self, inches: float) -> float:
        return inches * self.json_dpi

    def parse_graphviz_json(self, json):
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
            f"image size: {self.mapimage_width} {self.mapimage_height} {self.convert_pixels_to_inches(self.mapimage_width)} {self.convert_pixels_to_inches(self.mapimage_height)}"
        )
        for n in json['objects']:
            item = {}
            pos = n['pos'].split(',')
            item['key'] = n['name']
            item['height'] = self.convert_inches_to_pixels(float(n['height']))
            item['width'] = self.convert_inches_to_pixels(float(n['width']))
            item['pos_x'] = self.convert_points_to_pixels(float(pos[0]))
            item['pos_y'] = self.mapimage_height - (self.convert_points_to_pixels(float(pos[1])))
            item['pos_x1'] = item['pos_x'] - item['width'] / 2
            item['pos_y1'] = item['pos_y'] - item['height'] / 2
            item['pos_x2'] = item['pos_x'] + item['width'] / 2
            item['pos_y2'] = item['pos_y'] + item['height'] / 2
            self.json_clickable_objects[n['name']] = item
            print(f"clickable object: {n['name']} {item['pos_x']} {item['pos_y']} {item['width']} {item['height']}")
