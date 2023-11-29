"""Creates and manages the main UI of the application itself.

"""
from datetime import datetime
import flet as ft
from config import Config
from frontend import Frontend
from model import Step
from renderdot import RenderDot
from rendermarkdown import RenderMarkdown
from stepeditordialog import StepEditorDialog
from stepresourcelisteditor import StepResourceListEditor
from storage import Storage
from view import ViewStep


# TODO try to embed svg in markdown
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
# TODO create a "floating part view" where any part not mentioned in the steps but in the BOM is listed with a warning
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
# TODO display all uplink steps and parts
# TODO display all downwind steps and parts
# TODO display all parallel processes
# TODO maybe display and edit ALL steps in one markdown? Can we scroll to specific point?
# TODO display the process as a flowchart
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
        self.page.views[0].scroll = ft.ScrollMode.ADAPTIVE
        self.visible_step_key = None
        self.frontend = Frontend(self)
        self.ctrl = {}
        self.storage = Storage(self)
        self.renderdot = RenderDot(self)
        self.rendermarkdown = RenderMarkdown(self)
        self.long_process_depth = 0
        self.ctrl['main_topbar'] = ft.Container(visible=False)
        self.ctrl['main_leftbar'] = ft.Container(visible=False,rotate=90)
        self.ctrl['main_rightbar'] = ft.Container(visible=False,rotate=270)
        self.ctrl['main_bottombar'] = ft.Container(visible=False)
        self.ctrl['mainmarkdown'] = ft.Markdown(selectable=True,
                                                expand=False,
                                                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                                on_tap_link=self.markdown_link_tap)
        self.maincontent = ft.Container(bgcolor=ft.colors.ON_SECONDARY, expand=True)
        self.ctrl['maincontent']=self.maincontent
        #self.maincontent.content = ft.Column(expand=3,
        #                                     scroll=ft.ScrollMode.ALWAYS,
        #                                     controls=[self.ctrl['main_topbar'],
        #                                               ft.Row(controls=[
        #                                                   self.ctrl['main_leftbar'],
        #                                                   self.ctrl['mainmarkdown'],
        #                                                   self.ctrl['main_rightbar']],expand=True),
        #                                               self.ctrl['main_bottombar']])
        self.maincontent.content = ft.Column(expand=3,
                                             scroll=ft.ScrollMode.ALWAYS,
                                             controls=[
                                                 self.ctrl['main_topbar'],
                                                 self.ctrl['mainmarkdown'],
                                                 self.ctrl['main_bottombar'],
                                             ])

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
        self.ctrl['panel_searchresults'] = ft.Column(controls=[ft.Text('searchresults')],expand=True)
        self.ctrl['panel_searchresults_container'] = ft.Container(
            self.ctrl['panel_searchresults'],
            expand=True,
            width=200,
            margin=10,
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=10,
            visible=False,
            alignment=ft.alignment.top_center)

        url_emojiexamples = 'https://awes0mem4n.github.io/emojis-github.html'
        url_markdownsyntax = 'https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax'
        self.ctrl['emojihelp']: ft.IconButton = ft.IconButton(ft.icons.HELP,
                                                              on_click=lambda e: self.page.launch_url(
                                                                  url_emojiexamples),
                                                              tooltip='Emoji help')
        self.ctrl['markdownhelp']: ft.IconButton = ft.IconButton(ft.icons.HELP_CENTER,
                                                                 on_click=lambda e: self.page.launch_url(
                                                                     url_markdownsyntax),
                                                                 tooltip='Markdown help')
        self.ctrl |= {'progressring': ft.ProgressRing(visible=False),
                      'reload': ft.IconButton(ft.icons.REFRESH, on_click=self.click_refresh,
                                              tooltip='Reload datafiles'),
                      'feedback': ft.IconButton(ft.icons.FEEDBACK, tooltip='Send Feedback',
                                                on_click=lambda _: self.page.launch_url(Config.feedback_url)),
                      }
        page.appbar = ft.AppBar(
            title=ft.Text('Manufacturing Document Editor', color=Config.instance_color),
            center_title=False,  # we center the title
            bgcolor=Config.instance_bgcolor,  # a color for the AppBar's background
            actions=[self.ctrl['markdownhelp'], self.ctrl['emojihelp'], self.ctrl['contains'],
                     self.ctrl['progressring'],
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
            controls=[self.ctrl['panel_editor'], self.maincontent, self.ctrl['panel_searchresults_container']],
            vertical_alignment=ft.CrossAxisAlignment.START)
        self.ctrl['layout'] = self.layout
        self.page.controls.append(ft.Column(controls=[self.ctrl['toolbar'], self.layout, self.ctrl['footer']]))
        self.page.update()
        self.load_mainmarkdown_step('STEP-0001')

    def markdown_link_tap(self, event):
        print(f'Link tapped: {event.data}')
        if event.data.startswith('click://'):
            self.handle_click_link(event)
        else:
            self.page.launch_url(event.data)

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
            ft.Row(controls=[ft.Text('Search Results', style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                             ft.Container(expand=True),
                             ft.IconButton(ft.icons.CLOSE, on_click=self.hide_searchresults)]))
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
        self.ctrl['panel_searchresults_container'].visible = self.ctrl['check_panel_searchresults'].value
        self.ctrl['panel_searchresults_container'].update()

    def click_step_edit(self, e):
        del e
        self.editor_dialog = StepEditorDialog(self, self.storage.cache_steps.data[self.visible_step_key])
        self.page.dialog = self.editor_dialog.dialog
        self.page.dialog.visible = True
        self.page.dialog.open = True
        self.page.update()

    def click_step_edit_inputparts(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.inputparts,
                                     'parts', f'Input parts for {step.key}', is_inputpart=True)
        self.edit_popup_editordialog(dlg)

    def click_step_edit_outputparts(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.outputparts,
                                     'parts', f'Output parts for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_roles(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.roles, 'roles', f'Roles for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_tools(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.tools, 'tools', f'Tools used for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_machines(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.machines, 'machines', f'Machines used for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_consumables(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.consumables, 'consumables', f'Consumables used in {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_actions(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.actions, 'actions', f'Actions used for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_start_after(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.start_after, 'start_after',
                                     f'{step.key} dependencies start_after')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_start_after_start(self, e):
        del e
        step = self.storage.cache_steps.data[self.visible_step_key]
        dlg = StepResourceListEditor(self, step, step.start_after_start, 'start_after_start',
                                     f'Parallel dependencies for {step.key} start_after_start')
        self.edit_popup_editordialog(dlg)

    def edit_popup_editordialog(self, editor_dialog):
        self.editor_dialog = editor_dialog
        self.page.dialog = self.editor_dialog.dialog
        self.page.dialog.visible = True
        self.page.dialog.open = True
        self.page.update()

    def load_mainmarkdown_step(self, key):
        self.visible_step_key = key
        step=self.storage.cache_steps.data[key]
        self.ctrl['mainmarkdown'].value = self.rendermarkdown.render_step(step)
        #print(f'load_mainmarkdown {key}')
        top_controls = []
        self.prepare_top_dependency_buttons(top_controls, step)
        self.ctrl['main_topbar'].content = ft.Row(controls=top_controls)
        self.ctrl['main_topbar'].visible = True
        bottom_controls = []
        self.prepare_bottom_dependency_buttons(bottom_controls, step)
        self.ctrl['main_bottombar'].content = ft.Row(controls=bottom_controls)
        self.ctrl['main_bottombar'].visible = True
        #self.ctrl['main_bottombar'].content = ft.Text(f'{ViewStep.find_steps_depending_on_this(step, self.storage)}')
        #self.ctrl['main_leftbar'].content = ft.Text(f'{ViewStep.find_steps_after_start_with_this(step, self.storage)}')
        #self.ctrl['main_rightbar'].content = ft.Text(f'{ViewStep.find_steps_which_start_after_this_starts(step, self.storage)}')
        #self.ctrl['main_bottombar'].visible = True
        #self.ctrl['main_leftbar'].visible = True
        #self.ctrl['main_rightbar'].visible = True
        #print(f'ViewStep.find_steps_this_depends_on {ViewStep.find_steps_this_depends_on(step, self.storage)}')
        #print(f'ViewStep.find_steps_depending_on_this {ViewStep.find_steps_depending_on_this(step, self.storage)}')
        #print(f'ViewStep.find_steps_after_start_with_this {ViewStep.find_steps_after_start_with_this(step, self.storage)}')
        #print(f'ViewStep.find_steps_which_start_after_this_starts {ViewStep.find_steps_which_start_after_this_starts(step, self.storage)}')
        #self.ctrl['mainmarkdown'].update()
        self.ctrl['maincontent'].update()

    def prepare_bottom_dependency_buttons(self, control_list, step):
        start_after_start_controls = []
        start_after_finish = ViewStep.find_steps_depending_on_this(step, self.storage)
        start_after_finish = dict(sorted(start_after_finish.items()))

        start_after_start = ViewStep.find_steps_which_start_after_this_starts(step, self.storage)
        start_after_start = dict(sorted(start_after_start.items()))

        if len(start_after_finish) > 0:
            control_list.append(ft.Text(f'These must wait until {step.key} is done:'))
            for k in start_after_finish:
                control_list.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key)))
        for k in start_after_start:
            if k not in start_after_finish:
                start_after_start_controls.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key)))
        if len(start_after_start_controls) > 0:
            control_list.append(ft.Text(f'These can start in parallel after {step.key} starts:'))
            control_list.extend(start_after_start_controls)

    def prepare_top_dependency_buttons(self, control_list, step):
        start_after_start_controls = []
        start_after_start = ViewStep.find_steps_after_start_with_this(step, self.storage)
        start_after_start = dict(sorted(start_after_start.items()))
        start_after_finish = ViewStep.find_steps_this_depends_on(step, self.storage)
        start_after_finish = dict(sorted(start_after_finish.items()))
        if len(start_after_finish) > 0:
            control_list.append(ft.Text(f'{step.key} can start after these are all finished:'))
            for k in start_after_finish:
                control_list.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key)))
        for k in start_after_start:
            if k not in start_after_finish:
                start_after_start_controls.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key)))
        if len(start_after_start_controls) > 0:
            control_list.append(ft.Text(f'{step.key} can start together with these:'))
            control_list.extend(start_after_start_controls)

    def click_refresh(self, e):
        del e  # unused
        self.ctrl['progressring'].visible = True
        self.ctrl['progressring'].update()
        self.storage.load_resources()
        self.load_mainmarkdown_step(self.visible_step_key)
        # self.renderdot.render_bom_to_file()
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

    def handle_click_link(self, event):
        url = event.data
        # decode url parts (click://edit_step_inputparts/47)
        url = url.replace('click://', '')
        url_parts = url.split('/')
        if len(url_parts) < 2:
            return
        action = url_parts[0]
        # pk = url_parts[1]
        if action == 'step_edit':
            self.click_step_edit(None)
        elif action == 'step_edit_inputparts':
            self.click_step_edit_inputparts(None)
        elif action == 'step_edit_outputparts':
            self.click_step_edit_outputparts(None)
        elif action == 'step_edit_roles':
            self.click_step_edit_roles(None)
        elif action == 'step_edit_actions':
            self.click_step_edit_actions(None)
        elif action == 'step_edit_machines':
            self.click_step_edit_machines(None)
        elif action == 'step_edit_tools':
            self.click_step_edit_tools(None)
        elif action == 'step_edit_consumables':
            self.click_step_edit_consumables(None)
        elif action == 'step_edit_start_after':
            self.click_step_edit_start_after(None)
        elif action == 'step_edit_start_after_start':
            self.click_step_edit_start_after_start(None)
        else:
            print(f'Unknown action: {action}')
