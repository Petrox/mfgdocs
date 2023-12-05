"""Creates and manages the main UI of the application itself.

"""
import base64
from datetime import datetime
import flet as ft
from config import Config
from frontend import Frontend, Overview
from maindisplay import MainDisplay
from model import Step
from renderdot import RenderDot
from rendermarkdown import RenderMarkdown
from size_aware_control import SizeAwareControl
from stepeditordialog import StepEditorDialog
from stepresourcelisteditor import StepResourceListEditor
from storage import Storage
from view import ViewStep


# TODO convert main frame to be able to host the overview and the other views
# TODO zoom in and out seems to work only when the image is larger than the viewport, needs testing
# TODO remove all prints and use logging instead
# TODO add dangling outputs to a list that could be added to the input of a step
# TODO list all products that are built but have no steps to produce them so, one could add a step
# TODO list all bomitems that are not used in any step
# TODO list all parts that are bought but not used in any boms
# TODO add feature to group the inputlist of a step if the same part is not used by multiple times
# TODO add parameters (    Step-by-step instructions for each stage of production. Include specifics such as temperatures, pressures, and timings.)
#     packaging (    Details on how the finished product should be packaged. Instructions for shipping and handling.),
#     safety (    Safety guidelines for workers. Emergency procedures. Personal protective equipment (PPE) requirements.)
#     environment (    Information on how the manufacturing process affects the environment. Steps taken to minimize environmental impact.)
#     quality assurance: testing methods, machine maintenance text, required documentation texts to steps
#     compliance:     Information on compliance with industry standards and regulations. Certifications obtained for the product.
#     Troubleshooting Guide: Common issues during manufacturing and their solutions. Troubleshooting steps for equipment malfunctions.
#     Glossary: Definitions of terms used in the document.
#     References: Links to external resources. Additional supporting documents, such as material safety data sheets (MSDS) or CAD drawings.
#     Required signatures: everybody participating and the quality check / approval separately
#     Required measurement data: eg temperature, pressure, humidity, weight, etc
# TODO add markdown view for all resources
# TODO add json view and editor for all steps with the exception that the KEY can not change
# TODO add split action to the steps where the input and output parts and tools and other resources are all split and the step is duplicated with the same name and description
# TODO create a "unassociated part view" where any part not mentioned in the steps but in the BOM is listed with a warning
# TODO create a button to add a new step based on BOM data
# TODO add revisioning info (date, version, author, etc) for every change
# TODO add part specifications (eg dimensions, tolerances, material, etc) for part
# TODO add header and footer info to all reports
# TODO add git commit message for every change
# TODO document start_after
# TODO document start_after_start
# TODO document inputparts dependency
# TODO document outputparts dependency
# TODO while embedded links work and contain pk, the click handlers do not use the pk, but the visible element on screen
# TODO upload, manage, delete images
# TODO upload manage delete other files (?)
# TODO import from inventree
# TODO import images from inventree
# TODO check for minimal amounts (one input part at least, one role, one output part, etc)
# TODO check keyword: "requires" "suggests"  and "provides"
# TODO check that output parts must not be input parts
# TODO validate() step method with error display
# TODO markdown helpers for steps: warnings, errors, info, questionmark, checkmark, images etc
# TODO circular dependency detection (do we need it? maybe not)
# TODO optional Support decision points (Yes-No or multiple outcome) in the process and tag the output accordingly
# TODO maybe display and edit ALL steps in one markdown? Can we scroll to specific point?
# TODO display the process as a Gantt chart
# TODO display the process as a Kanban board
# TODO display the process as a calendar
# TODO display the process as a list
# TODO generate every single step and resource as a separate document
# TODO generate every single step as a separate document with all referred objects included
# TODO generate full map of all steps and resources
# TODO generate all steps in one document with internal links
# TODO generate all steps at one location in one document with internal links and all referred objects included
# TODO all printed material should have a QR code that links to the online version
# TODO all printed materials should have a document id/date/version in the footer
# TODO all generated reports should be stored as file and as database entry to reproduce them later
# TODO optional handle "build orders" (eg a list of steps to be done and generate a document with all steps and resources for each company involved)
# TODO optional integration so that external companies can be invited to participate in the process and their process steps can be tracked and followed (eg send an email with links to steps)
# TODO optional integration handle availability of resources (machines, tools, roles, actions), maybe with a calendar integration, or a calendar view
# TODO optional integration generate calendar events for all steps via shared calendar (and update it along the way)
# TODO optional integration generate a list of steps to be done today (every day) and send it via email or chat to participants


class MFGDocsApp:
    """Holder of the "page" object, handling all the necessary setup and functionality of the global UI.
    """
    ctrl: dict[str, ft.Control]
    page: ft.Page = None

    def __init__(self, page):
        self.editor_dialog = None
        self.page = page
        self.configure_page()
        self.visible_step_key = None
        self.frontend = Frontend(self)
        self.ctrl = {}
        self.storage = Storage(self)
        self.overview = Overview(self)
        self.renderdot = RenderDot(self)
        self.rendermarkdown = RenderMarkdown(self)
        self.long_process_depth = 0

        # self.maincontent = ft.Container(bgcolor=ft.colors.ON_SECONDARY, expand=True)
        self.maincontent = SizeAwareControl(expand=True)
        self.ctrl['maincontent'] = self.maincontent
        self.main_display = MainDisplay(self, self.storage)

        # self.maincontent.content = ft.Container(bgcolor=ft.colors.ON_SECONDARY,expand=True)
        self.maincontent.content = self.main_display.build()

        self.ctrl['contains'] = ft.TextField(
            label='Search here', width=150, color='black', border=ft.InputBorder.NONE,
            filled=True, dense=True, icon=ft.icons.SEARCH, on_submit=self.search
            )
        self.ctrl['panel_editor'] = ft.Column(controls=[ft.Text('editor')], visible=False)
        self.ctrl['panel_searchresults'] = ft.Column(controls=[ft.Text('searchresults')], expand=True)
        self.ctrl['panel_searchresults_container'] = ft.Container(
            self.ctrl['panel_searchresults'],
            expand=True,
            width=200,
            margin=10,
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=10,
            visible=False,
            alignment=ft.alignment.top_center
        )

        url_emojiexamples = 'https://awes0mem4n.github.io/emojis-github.html'
        url_markdownsyntax = 'https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax'

        self.ctrl['icon_emojihelp']: ft.IconButton = ft.IconButton(
            ft.icons.HELP,
            on_click=lambda e: self.page.launch_url(
                url_emojiexamples
            ),
            tooltip='Emoji help'
            )
        self.ctrl['icon_markdownhelp']: ft.IconButton = ft.IconButton(
            ft.icons.HELP_CENTER,
            on_click=lambda e: self.page.launch_url(
                url_markdownsyntax
            ),
            tooltip='Markdown help'
            )

        self.ctrl['icon_overview_button']: ft.IconButton = ft.IconButton(
            ft.icons.MAP,
            icon_color=ft.colors.ON_SECONDARY,
            on_click=self.click_overview,
            tooltip='Overview'
            )

        self.ctrl['progressring'] = ft.ProgressRing(visible=False)
        self.ctrl['icon_reload'] = ft.IconButton(
            ft.icons.REFRESH,
            on_click=self.click_reload_data_from_json,
            tooltip='Reload datafiles'
            )
        self.ctrl['icon_feedback'] = ft.IconButton(
            ft.icons.FEEDBACK,
            tooltip='Send Feedback',
            on_click=lambda _: self.page.launch_url(Config.feedback_url)
            )
        page.appbar = ft.AppBar(
            title=ft.Text(
                'Manufacturing Document Editor',
                color=Config.instance_color
                ),
            center_title=False,
            bgcolor=Config.instance_bgcolor,
            actions=[self.ctrl['progressring'],
                     self.ctrl['icon_overview_button'],
                     self.ctrl['icon_markdownhelp'],
                     self.ctrl['icon_emojihelp'],
                     self.ctrl['contains'],
                     self.ctrl['icon_reload'],
                     self.ctrl['icon_feedback']]
        )

        self.ctrl['log_message'] = ft.Text('')
        self.ctrl['footer'] = ft.Row(controls=[self.ctrl['log_message']])
        self.layout = ft.Container()
        self.layout.content = ft.Row(
            controls=[self.ctrl['panel_editor'], self.maincontent, self.ctrl['panel_searchresults_container']],
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        self.ctrl['layout'] = self.layout
        self.page.controls.append(ft.Column(controls=[self.layout, self.ctrl['footer']]))
        self.page.update()
        self.load_mainmarkdown_step('STEP-0001')

    def click_overview(self, event):
        del event
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.renderdot.render_steps_to_file()
        self.ctrl['progressring'].visible = False
        self.ctrl['progressring'].update()
        self.display_overview()

    def configure_page(self):
        self.page.title = 'MFGDocs'
        self.page.theme_mode = ft.ThemeMode.DARK
        scrollbar = ft.theme.ScrollbarTheme(
            thumb_visibility=True, thickness=10, track_visibility=True,
            interactive=True
            )
        self.page.theme = ft.theme.Theme(
            color_scheme_seed='blue',
            scrollbar_theme=scrollbar,
            visual_density=ft.ThemeVisualDensity.COMPACT,
            font_family='Roboto'
            )
        self.page.views[0].scroll = ft.ScrollMode.ADAPTIVE


    def show_searchresults(self):
        self.ctrl['check_panel_searchresults'].value = True
        self.ctrl['check_panel_searchresults'].update()
        self.ctrl['panel_searchresults_container'].visible = True
        self.ctrl['panel_searchresults_container'].width = 300
        self.ctrl['panel_searchresults_container'].update()

    def hide_searchresults(self, e):
        del e
        self.ctrl['check_panel_searchresults'].value = False
        self.ctrl['check_panel_searchresults'].update()
        self.ctrl['panel_searchresults_container'].visible = False
        self.ctrl['panel_searchresults_container'].update()

    def search(self, event):
        del event
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.ctrl['panel_searchresults'].controls.clear()
        self.ctrl['panel_searchresults'].controls.append(
            ft.Row(
                controls=[ft.Text('Search Results', style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                          ft.Container(expand=True),
                          ft.IconButton(ft.icons.CLOSE, on_click=self.hide_searchresults)]
                )
        )
        self.show_searchresults()
        results = 0
        for k, v in self.storage.cache_steps.data.items():
            assert isinstance(v, Step)
            if v.contains(self.ctrl['contains'].value):
                results += 1
                button = self.frontend.get_searchresultitem_step(k)
                button.on_click = lambda e, key=k: self.load_mainmarkdown_step(key)
                self.ctrl['panel_searchresults'].controls.append(button)
        if results == 0:
            self.ctrl['panel_searchresults'].controls.clear()
            self.ctrl['panel_searchresults'].controls.append(
                ft.Text(
                    'No search results found', color='red',
                    style=ft.TextThemeStyle.HEADLINE_MEDIUM
                    )
                )
        self.ctrl['panel_searchresults'].update()
        self.ctrl['progressring'].visible = False
        self.ctrl['progressring'].update()

    def load_mainmarkdown_step(self, key):
        step = self.storage.cache_steps.data[key]
        self.main_display.display_step(step)
        self.maincontent.update()

    def click_reload_data_from_json(self, e):
        del e  # unused
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.storage.load_resources()
        self.load_mainmarkdown_step(self.visible_step_key)
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

    def display_overview(self):
        self.page.dialog = self.overview.get_overview_dialog()
        self.page.dialog.visible = True
        self.page.update()
