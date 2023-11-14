"""Creates and manages the main UI of the application itself.

"""
from datetime import datetime
import flet as ft
from config import Config
from frontend import Frontend
from model import Step
from renderdot import RenderDot
from rendermarkdown import RenderMarkdown
from storage import Storage


class MFGDocsApp:
    """Holder of the "page" object, handling all the necessary setup and functionality of the global UI.
    """
    ctrl: dict[str, ft.Control]
    page: ft.Page = None

    def __init__(self, page):
        self.frontend = Frontend(self)
        self.ctrl = {}
        self.storage = Storage(self)
        self.renderdot = RenderDot(self)
        self.rendermarkdown = RenderMarkdown(self)
        self.long_process_depth = 0
        self.ctrl['mainmarkdown'] = ft.Markdown(selectable=True,extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
        self.maincontent = ft.Container(bgcolor=ft.colors.ON_SECONDARY,expand=True)
        self.maincontent.content = self.ctrl['mainmarkdown']
        self.page = page
        self.page.title = 'MFGDocs'
        self.page.theme_mode = ft.ThemeMode.DARK
        scrollbar = ft.theme.ScrollbarTheme(thumb_visibility=True, thickness=10, track_visibility=True,
                                            interactive=True)
        self.page.theme = ft.theme.Theme(color_scheme_seed='blue',
                                         scrollbar_theme=scrollbar,
                                         visual_density=ft.ThemeVisualDensity.COMPACT,
                                         font_family='Roboto')
        self.ctrl['contains'] = ft.TextField(label='Search here', width=150, color='black', border=ft.InputBorder.NONE,
                                             filled=True, dense=True, icon=ft.icons.SEARCH, on_submit=self.search)
        self.ctrl['panel_editor'] = ft.Column(controls=[ft.Text('editor')], visible=False)
        self.ctrl['panel_searchresults'] = ft.Column(controls=[ft.Text('searchresults')], visible=False)

        self.ctrl |= {'progressring': ft.ProgressRing(visible=False),
                      'reload': ft.IconButton(ft.icons.REFRESH, on_click=self.click_refresh),
                      'feedback': ft.IconButton(ft.icons.FEEDBACK,
                                                on_click=lambda _: self.page.launch_url(Config.feedback_url)),
                      }
        page.appbar = ft.AppBar(
            title=ft.Text('Manufacturing Document Editor', color=Config.instance_color),
            center_title=False,  # we center the title
            bgcolor=Config.instance_bgcolor,  # a color for the AppBar's background
            actions=[self.ctrl['contains'], self.ctrl['progressring'],
                     self.ctrl['reload'], self.ctrl['feedback']]
        )
        self.ctrl['check_view_all'] = ft.Checkbox(label='View all')
        self.ctrl['check_view_names'] = ft.Checkbox(label='View names')
        self.ctrl['check_group_activities'] = ft.Checkbox(label='Group activities')
        self.ctrl['check_group_locations'] = ft.Checkbox(label='Group locations')
        self.ctrl['check_panel_editor'] = ft.Checkbox(label='Editor', on_change=self.click_check_panel_editor)
        self.ctrl['check_panel_searchresults'] = ft.Checkbox(label='Results',
                                                             on_change=self.click_check_panel_searchresults)
        self.ctrl['toolbar_checkboxes'] = ft.Row(controls=[self.ctrl['check_panel_editor'],
                                                           self.ctrl['check_panel_searchresults'],
                                                           ft.VerticalDivider(),
                                                           self.ctrl['check_view_all'],
                                                           self.ctrl['check_view_names'],
                                                           self.ctrl['check_group_activities'],
                                                           self.ctrl['check_group_locations']])

        self.ctrl['toolbar'] = ft.Row(controls=[self.ctrl['toolbar_checkboxes']])

        self.ctrl['log_message'] = ft.Text('')
        self.ctrl['footer'] = ft.Row(controls=[self.ctrl['log_message']])
        self.layout = ft.Container()
        self.layout.content = ft.Row(
            controls=[self.ctrl['panel_editor'], self.maincontent, self.ctrl['panel_searchresults']])
        self.ctrl['layout'] = self.layout
        self.page.controls.append(ft.Column(controls=[self.ctrl['toolbar'], self.layout, self.ctrl['footer']]))
        self.page.update()
        self.load_mainmarkdown('STEP-0001')

    def search(self, event):
        del event
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.ctrl['panel_searchresults'].visible = True
        self.ctrl['panel_searchresults'].controls.clear()
        self.ctrl['panel_searchresults'].controls.append(ft.Text('Search Results',
                                                                 style=ft.TextThemeStyle.HEADLINE_MEDIUM))
        self.ctrl['check_panel_searchresults'].value = True
        self.ctrl['check_panel_searchresults'].update()
        self.ctrl['panel_searchresults'].update()
        results = 0
        for k, v in self.storage.cache_steps.data.items():
            assert isinstance(v, Step)
            if v.contains(self.ctrl['contains'].value):
                results += 1
                self.ctrl['panel_searchresults'].controls.append(self.frontend.get_searchresultitem_step(k))
        if results == 0:
            self.ctrl['panel_searchresults'].controls.clear()
            self.ctrl['panel_searchresults'].controls.append(ft.Text('No search results found', color='red',
                                                                     style=ft.TextThemeStyle.HEADLINE_MEDIUM))
        self.ctrl['panel_searchresults'].update()
        self.ctrl['progressring'].visible = False
        self.ctrl['progressring'].update()

    def click_check_panel_editor(self, event):
        del event  # unused
        self.ctrl['panel_editor'].visible = self.ctrl['check_panel_editor'].value
        self.ctrl['panel_editor'].update()

    def click_check_panel_searchresults(self, event):
        del event  # unused
        self.ctrl['panel_searchresults'].visible = self.ctrl['check_panel_searchresults'].value
        self.ctrl['panel_searchresults'].update()


    def load_mainmarkdown(self,key):
        self.ctrl['mainmarkdown'].value=self.rendermarkdown.render_step(self.storage.cache_steps.data[key])
        self.ctrl['mainmarkdown'].update()

    def click_refresh(self, e):
        del e  # unused
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.storage.load_resources()
        self.renderdot.render_bom_to_file()
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
