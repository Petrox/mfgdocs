"""Creates and manages the main UI of the application itself.

"""
import time
from datetime import datetime
import flet as ft
from config import Config


class MFGDocsApp:
    """Holder of the "page" object, handling all the necessary setup and functionality of the global UI.
    """
    ctrl: dict[str, ft.Control]
    page: ft.Page = None

    def __init__(self, page):
        self.maincontent = ft.Container()
        self.page = page
        self.page.title = 'MFGDocs'
        self.storage = {}
        self.ctrl = {'progressring': ft.ProgressRing(visible=False),
                     'reload': ft.IconButton(ft.icons.REFRESH, on_click=self.click_refresh)}
        self.long_process_depth = 0
        page.appbar = ft.AppBar(
            title=ft.Text('Markdown Editor', color=Config.instance_color),  # title of the AppBar, with a white color
            center_title=True,  # we center the title
            bgcolor=Config.instance_bgcolor,  # a color for the AppBar's background
            actions=[self.ctrl['progressring'], self.ctrl['reload'], self.ctrl['entities']]
        )
        self.maincontent.content = ft.Text('maincontent')
        self.page.controls.append(self.maincontent)
        self.page.update()

    def click_refresh(self, e):
        del e  # unused
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        time.sleep(2)
        self.ctrl['progressring'].visible = False
        self.ctrl['progressring'].update()

    def longprocess_start(self):
        assert isinstance(self.maincontent, ft.Container)
        self.long_process_depth += 1
        if self.long_process_depth > 0:
            self.maincontent.animate_opacity = 100
            self.maincontent.disabled = True
            self.maincontent.opacity = 0.2
            self.maincontent.update()

    def longprocess_finish(self):
        assert isinstance(self.maincontent, ft.Container)
        self.long_process_depth -= 1
        if self.long_process_depth < 1:
            self.maincontent.animate_opacity = 100
            self.maincontent.disabled = False
            self.maincontent.opacity = 1.0
            self.maincontent.update()

    def log(self, message):
        print(f"[{datetime.now().isoformat()}] {message}")

    def main(self):
        pass
