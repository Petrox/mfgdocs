import flet as ft
from model import Step
from stepeditordialog import StepEditorDialog
from stepresourcelisteditor import StepResourceListEditor
from view import ViewStep


class MainDisplay:

    def __init__(self, mfgdocsapp: 'MFGDocsApp', storage: 'Storage'):
        self.editor_dialog = None
        self.mfgdocsapp = mfgdocsapp
        self.storage = storage
        self.ctrl = {}
        self.maincontrol = ft.Container()
        self.object_on_display = None

    def build(self):
        self.ctrl['maincontrol'] = self.maincontrol
        self.ctrl['step_topbar'] = ft.Container(visible=False)
        self.ctrl['step_bottombar'] = ft.Container(visible=False)
        self.ctrl['step_markdown'] = ft.Markdown(
            selectable=True,
            expand=False,
            value='ASDASDASD',
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=self.markdown_link_tap
        )
        self.ctrl['map_check_view_all'] = ft.Checkbox(label='View all')
        self.ctrl['map_check_show_names'] = ft.Checkbox(label='Show names')
        self.ctrl['map_check_show_warnings'] = ft.Checkbox(label='Show warnings')
        self.ctrl['map_check_show_bom'] = ft.Checkbox(label='Show BOM')
        self.ctrl['map_check_show_orphans'] = ft.Checkbox(label='Show Orphans')
        self.ctrl['map_check_show_subparts'] = ft.Checkbox(label='Show Subparts')
        self.ctrl['map_check_group_companies'] = ft.Checkbox(label='Group companies')
        self.ctrl['map_check_group_activities'] = ft.Checkbox(label='Group activities')
        self.ctrl['map_check_group_locations'] = ft.Checkbox(label='Group locations')
        self.ctrl['map_toolbar_checkboxes'] = ft.Row(
            controls=[self.ctrl['map_check_view_all'],
                      self.ctrl['map_check_show_names'],
                      self.ctrl['map_check_show_warnings'],
                      self.ctrl['map_check_show_bom'],
                      self.ctrl['map_check_show_orphans'],
                      self.ctrl['map_check_show_subparts'],
                      ft.VerticalDivider(),
                      self.ctrl['map_check_group_companies'],
                      self.ctrl['map_check_group_activities'],
                      self.ctrl['map_check_group_locations']]
        )

        self.ctrl['map_toolbar'] = ft.Row(controls=[self.ctrl['map_toolbar_checkboxes']])
        self.ctrl['map_canvas'] = ft.Container(ft.Text('map canvas'), bgcolor='lightblue')
        self.ctrl['map_display'] = ft.Column(
            controls=[self.ctrl['map_toolbar'],
                      self.ctrl['map_canvas']]
        )

        self.ctrl['step_display'] = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                self.ctrl['step_topbar'],
                self.ctrl['step_markdown'],
                self.ctrl['step_bottombar']
            ]
        )

        self.ctrl['maincontrol'].content = ft.Stack(controls=[self.ctrl['map_display'], self.ctrl['step_display']])
        return self.maincontrol

    def markdown_link_tap(self, event):
        print(f'Link tapped: {event.data}')
        if event.data.startswith('click://'):
            self.handle_click_link(event)
        else:
            self.mfgdocsapp.page.launch_url(event.data)

    def display_step(self, step: Step):
        self.object_on_display = step
        self.ctrl['map_display'].visible = False
        self.ctrl['step_display'].visible = True
        self.ctrl['step_markdown'].value = self.mfgdocsapp.rendermarkdown.render_step(step)
        self.ctrl['step_topbar'].content = ft.Row(controls=self.prepare_top_dependency_buttons(step))
        self.ctrl['step_topbar'].visible = True
        self.ctrl['step_bottombar'].content = ft.Row(controls=self.prepare_bottom_dependency_buttons(step))
        self.ctrl['step_bottombar'].visible = True
        self.maincontrol.update()

    def prepare_bottom_dependency_buttons(self, step):
        control_list = []
        start_after_start_controls = []
        start_after_finish = ViewStep.find_steps_depending_on_this(step, self.storage)
        start_after_finish = dict(sorted(start_after_finish.items()))
        start_after_start = ViewStep.find_steps_which_start_after_this_starts(step, self.storage)
        start_after_start = dict(sorted(start_after_start.items()))

        if len(start_after_finish) > 0:
            control_list.append(ft.Text(f'These must wait until {step.key} is done:'))
            for k in start_after_finish:
                control_list.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key))
                )
        for k in start_after_start:
            if k not in start_after_finish:
                start_after_start_controls.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key))
                )
        if len(start_after_start_controls) > 0:
            control_list.append(ft.Text(f'These can start in parallel after {step.key} starts:'))
            control_list.extend(start_after_start_controls)
        return control_list

    def prepare_top_dependency_buttons(self, step):
        control_list = []
        start_after_start_controls = []
        start_after_start = ViewStep.find_steps_after_start_with_this(step, self.storage)
        start_after_start = dict(sorted(start_after_start.items()))
        start_after_finish = ViewStep.find_steps_this_depends_on(step, self.storage)
        start_after_finish = dict(sorted(start_after_finish.items()))
        if len(start_after_finish) > 0:
            control_list.append(ft.Text(f'{step.key} can start after these are all finished:'))
            for k in start_after_finish:
                control_list.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key))
                )
        for k in start_after_start:
            if k not in start_after_finish:
                start_after_start_controls.append(
                    ft.ElevatedButton(f'{k}', on_click=lambda e, key=k: self.load_mainmarkdown_step(key))
                )
        if len(start_after_start_controls) > 0:
            control_list.append(ft.Text(f'{step.key} can start together with these:'))
            control_list.extend(start_after_start_controls)
        return control_list

    def handle_click_link(self, event):
        url = event.data
        # decode url parts (click://edit_step_inputparts/47)
        url = url.replace('click://', '')
        url_parts = url.split('/')
        print(f'handle_click_link: {url_parts}')
        if len(url_parts) < 2:
            return
        action = url_parts[0]
        # pk = url_parts[1]
        if action == 'step_edit':
            self.click_step_edit(url_parts)
        elif action == 'step_edit_inputparts':
            self.click_step_edit_inputparts(url_parts)
        elif action == 'step_edit_outputparts':
            self.click_step_edit_outputparts(url_parts)
        elif action == 'step_edit_roles':
            self.click_step_edit_roles(url_parts)
        elif action == 'step_edit_actions':
            self.click_step_edit_actions(url_parts)
        elif action == 'step_edit_machines':
            self.click_step_edit_machines(url_parts)
        elif action == 'step_edit_tools':
            self.click_step_edit_tools(url_parts)
        elif action == 'step_edit_consumables':
            self.click_step_edit_consumables(url_parts)
        elif action == 'step_edit_start_after':
            self.click_step_edit_start_after(url_parts)
        elif action == 'step_edit_start_after_start':
            self.click_step_edit_start_after_start(url_parts)
        else:
            print(f'Unknown action: {action}')

    def click_step_edit_actions(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display

        dlg = StepResourceListEditor(self.mfgdocsapp, step, step.actions, 'actions', f'Actions used for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_consumables(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display

        dlg = StepResourceListEditor(self.mfgdocsapp, step, step.consumables, 'consumables', f'Consumables used in {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_tools(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display
        dlg = StepResourceListEditor(self.mfgdocsapp, step, step.tools, 'tools', f'Tools used for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_roles(self, url_parts: list[str]):
        print(f'click_step_edit_roles: {url_parts} {self.object_on_display}')
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display
        dlg = StepResourceListEditor(self.mfgdocsapp, step, step.roles, 'roles', f'Roles for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_inputparts(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display
        dlg = StepResourceListEditor(
            self.mfgdocsapp, step, step.inputparts,
            'parts', f'Input parts for {step.key}', is_inputpart=True
        )
        self.edit_popup_editordialog(dlg)

    def click_step_edit(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display
        self.editor_dialog = StepEditorDialog(self.mfgdocsapp, step)
        self.mfgdocsapp.page.dialog = self.editor_dialog.dialog
        self.mfgdocsapp.page.dialog.visible = True
        self.mfgdocsapp.page.dialog.open = True
        self.mfgdocsapp.page.update()

    def click_step_edit_outputparts(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display

        dlg = StepResourceListEditor(
            self.mfgdocsapp, step, step.outputparts,
            'parts', f'Output parts for {step.key}'
        )
        self.edit_popup_editordialog(dlg)

    def click_step_edit_machines(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display

        dlg = StepResourceListEditor(self.mfgdocsapp, step, step.machines, 'machines', f'Machines used for {step.key}')
        self.edit_popup_editordialog(dlg)

    def click_step_edit_start_after(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display

        dlg = StepResourceListEditor(
            self.mfgdocsapp, step, step.start_after, 'start_after',
            f'{step.key} dependencies start_after'
        )
        self.edit_popup_editordialog(dlg)

    def click_step_edit_start_after_start(self, url_parts: list[str]):
        del url_parts
        if self.object_on_display is None:
            return
        if not isinstance(self.object_on_display,Step):
            return
        step = self.object_on_display

        dlg = StepResourceListEditor(
            self.mfgdocsapp, step, step.start_after_start, 'start_after_start',
            f'Parallel dependencies for {step.key} start_after_start'
        )
        self.edit_popup_editordialog(dlg)

    def edit_popup_editordialog(self, editor_dialog):
        self.editor_dialog = editor_dialog
        self.mfgdocsapp.page.dialog = self.editor_dialog.dialog
        self.mfgdocsapp.page.dialog.visible = True
        self.mfgdocsapp.page.dialog.open = True
        self.mfgdocsapp.page.update()

    def display_map(self):
        self.object_on_display = None
        self.ctrl['map_display'].visible = True
        self.ctrl['step_display'].visible = False
        self.maincontrol.update()

    def load_mainmarkdown_step(self, key):
        step = self.storage.cache_steps.data[key]
        self.display_step(step)
