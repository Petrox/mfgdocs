"""Builds and handles the step editor dialog.

Use the dialog property to access the dialog control.
"""
import copy

import flet as ft
from model import Step
from ingredidentlisteditor import IngredientListEditor



class StepEditorDialog:
    """Builds and handles the step editor dialog.
    """
    dialog: ft.AlertDialog
    original_step: dict

    def __init__(self, mfgdocsapp: 'MFGDocsApp', step: Step):
        self.mfgdocsapp = mfgdocsapp
        self.step = step
        self.original_step = copy.deepcopy(step.to_dict())
        self.dialog = ft.AlertDialog(modal=False)
        self.dialog.title = ft.Text(f'Step Editor {self.step.key}')
        self.dialog.content = self.get_content()
        self.dialog.actions = [ft.TextButton('Cancel', on_click=self.dialog_cancel),
                               ft.TextButton('Preview', on_click=self.dialog_preview),
                               ft.TextButton('Save', on_click=self.dialog_save)]
        self.dialog.actions_alignment = 'end'
        self.dialog.shape = ft.BeveledRectangleBorder()

        self.dialog.visible = True

    def get_content(self):
        return ft.Container(expand=True,
                            content=ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, width=800,
                                              controls=[
                                                  ft.TextField(label='Name', dense=True, value=self.step.name,
                                                               on_change=lambda e: setattr(self.step, 'name',
                                                                                           e.control.value)),
                                                  ft.TextField(label='Description', dense=True, multiline=True,
                                                               min_lines=2, max_lines=20, value=self.step.description,
                                                               on_change=lambda e: setattr(self.step, 'description',
                                                                                           e.control.value)),
                                                  ft.TextField(label='Acceptance criteria', dense=True, multiline=True,
                                                               min_lines=1, max_lines=6, value=self.step.acceptance,
                                                               on_change=lambda e: setattr(self.step, 'acceptance',
                                                                                           e.control.value)),
                                                  ft.TextField(label='Prepare hours', dense=True,
                                                               value=self.step.prepare_hours,
                                                               on_change=lambda e: setattr(self.step, 'prepare_hours',
                                                                                           e.control.value)),
                                                  ft.TextField(label='Cooldown hours', dense=True,
                                                               value=self.step.cooldown_hours,
                                                               on_change=lambda e: setattr(self.step, 'cooldown_hours',
                                                                                           e.control.value)),
                                                  IngredientListEditor('Input parts',self.step.inputparts)
                                                  # ft.TextField(label='Location', value=self.step.location,
                                                  # on_change=self.change_location),
                                                  # ft.TextField(label='Start after', value=self.step.start_after,
                                                  # on_change=self.change_start_after),
                                                  # ft.TextField(label='Start after start',
                                                  # value=self.step.start_after_start,
                                                  # on_change=self.change_start_after_start),
                                                  # ft.TextField(label='Input parts', value=self.step.inputparts,
                                                  # on_change=self.change_inputparts),
                                                  # ft.TextField(label='Output parts', value=self.step.outputparts,
                                                  # on_change=self.change_outputparts),
                                                  # ft.TextField(label='Tools',
                                                  # value=self.step.tools, on_change=self.change_tools),
                                                  # ft.TextField(label='Machines',
                                                  # value=self.step.machines, on_change=self.change_machines),
                                                  # ft.TextField(label='Roles',
                                                  # value=self.step.roles, on_change=self.change_roles),
                                                  # ft.TextField(label='Actions',
                                                  # value=self.step.actions, on_change=self.change_actions),
                                                  # ft.TextField(label='Consumables', value=self.step.consumables,
                                                  # on_change=self.change_consumables),
                                              ]))

    def dialog_cancel(self, e):
        del e
        self.dialog.open = False
        self.step.from_dict(self.original_step)
        self.parent_search_update()
        self.parent_markdown_update()
        self.mfgdocsapp.page.update()

    def dialog_save(self, e):
        del e
        self.dialog.open = False
        self.parent_search_update()
        self.parent_markdown_update()
        self.mfgdocsapp.page.update()

    def parent_markdown_update(self):
        self.mfgdocsapp.load_mainmarkdown(self.step.key)

    def parent_search_update(self):
        if self.mfgdocsapp.ctrl['panel_searchresults_container'].visible:
            self.mfgdocsapp.search(None)

    def dialog_preview(self, e):
        del e
        self.parent_search_update()
        self.parent_markdown_update()
        self.mfgdocsapp.page.update()
