"""Creates and manages the main UI of the application itself.

"""
import time
from datetime import datetime
import flet as ft
from config import Config
from storage import Storage


class MFGDocsApp:
    """Holder of the "page" object, handling all the necessary setup and functionality of the global UI.
    """
    ctrl: dict[str, ft.Control]
    page: ft.Page = None

    def __init__(self, page):
        self.maincontent = ft.Container()
        self.page = page
        self.page.title = 'MFGDocs'
        self.page.theme_mode=ft.ThemeMode.DARK
        scrollbar = ft.theme.ScrollbarTheme(thumb_visibility=True, thickness=10, track_visibility=True,
                                                  interactive=True)
        self.page.theme=ft.theme.Theme(color_scheme_seed='blue',
                                       scrollbar_theme=scrollbar,
                                       visual_density=ft.ThemeVisualDensity.COMPACT,
                                       font_family='Roboto')
        self.storage = Storage(self)
        self.ctrl = {'progressring': ft.ProgressRing(visible=False),
                     'reload': ft.IconButton(ft.icons.REFRESH, on_click=self.click_refresh)}
        self.long_process_depth = 0
        page.appbar = ft.AppBar(
            title=ft.Text('Manufacturing Document Editor', color=Config.instance_color),
            center_title=True,  # we center the title
            bgcolor=Config.instance_bgcolor,  # a color for the AppBar's background
            actions=[self.ctrl['progressring'], self.ctrl['reload']]
        )
        self.ctrl['step_contains'] = ft.TextField(label='Step search', width=100)
        self.ctrl['step_search'] = ft.IconButton(ft.icons.SEARCH)
        self.ctrl['step_dropdown'] = ft.Dropdown(width=160)
        self.ctrl['part_contains'] = ft.TextField(label='Part search', width=100)
        self.ctrl['part_search'] = ft.IconButton(ft.icons.SEARCH)
        self.ctrl['part_dropdown'] = ft.Dropdown(width=160)
        self.ctrl['check_view_all'] = ft.Checkbox(label='View all')
        self.ctrl['check_view_names'] = ft.Checkbox(label='View names')
        self.ctrl['check_group_activities'] = ft.Checkbox(label='Group activities')
        self.ctrl['check_group_locations'] = ft.Checkbox(label='Group locations')
        self.ctrl['toolbar_checkboxes'] = ft.Row(controls=[self.ctrl['check_view_all'],
                                                           self.ctrl['check_view_names'],
                                                           self.ctrl['check_group_activities'],
                                                           self.ctrl['check_group_locations']])
        self.ctrl['toolbar'] = ft.Row(controls=[self.ctrl['step_contains'],
                                                          self.ctrl['step_search'],
                                                          self.ctrl['step_dropdown'],
                                                          self.ctrl['part_contains'],
                                                          self.ctrl['part_search'],
                                                          self.ctrl['part_dropdown'],
                                                          self.ctrl['toolbar_checkboxes']])

        self.ctrl['log_message'] = ft.Text('')
        self.ctrl['footer'] = ft.Row(controls=[self.ctrl['log_message']])

        self.maincontent.content = ft.Text('maincontent')
        self.page.controls.append(ft.Column(controls=[self.ctrl['toolbar'],self.maincontent,self.ctrl['footer']]))
        self.page.update()

    def click_refresh(self, e):
        del e  # unused
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.storage.load_resources()
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
