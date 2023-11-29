"""Builds and handles the step editor dialog.

Use the dialog property to access the dialog control.
"""
import copy

import flet as ft
from model import Step


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
                               #ft.TextButton('Preview', on_click=self.dialog_preview),
                               ft.TextButton('Save', on_click=self.dialog_save)]
        self.dialog.actions_alignment = 'end'
        self.dialog.shape = ft.BeveledRectangleBorder()

        self.dialog.visible = True

    def get_content(self):
        control_list = [
            ft.TextField(label='Name', dense=True, value=self.step.name,
                         on_change=lambda e: setattr(self.step, 'name', e.control.value)),
            ft.Dropdown(label='Location', dense=True, value=self.step.location,
                        options=list(
                            map(lambda x: ft.dropdown.Option(x.key, x.key + ' - ' + x.name),
                                self.mfgdocsapp.storage.cache_locations.data.values())),
                        on_change=lambda e: setattr(self.step, 'location', e.control.value)
                        ),
            ft.Dropdown(label='Responsible company', dense=True, value=self.step.company,
                        options=list(
                            map(lambda x: ft.dropdown.Option(x.key, x.key + ' - ' + x.name),
                                self.mfgdocsapp.storage.cache_companies.data.values())),
                        on_change=lambda e: setattr(self.step, 'company',e.control.value)
                        ),
            ft.TextField(label='Description', dense=True, multiline=True,
                         min_lines=2, max_lines=20, value=self.step.description,
                         on_change=lambda e: setattr(self.step, 'description',e.control.value)),
            ft.TextField(label='Prepare', dense=True, multiline=True,
                         min_lines=2, max_lines=20, value=self.step.prepare_text,
                         on_change=lambda e: setattr(self.step, 'prepare_text',e.control.value)),
            ft.TextField(label='Acceptance criteria', dense=True, multiline=True,
                         min_lines=1, max_lines=6, value=self.step.acceptance,
                         on_change=lambda e: setattr(self.step, 'acceptance',e.control.value)),
            ft.Dropdown(label='What if quality check fails?', dense=True, value=self.step.qcfailstep,
                        options=list(
                            map(lambda x: ft.dropdown.Option(x.key, x.key + ' - ' + x.name),
                                self.mfgdocsapp.storage.cache_steps.data.values())),
                        on_change=lambda e: setattr(self.step, 'qcfailstep', e.control.value)
                        ),
            ft.Checkbox(label='All Outputs are final', value=self.step.final,
                        on_change=lambda e: setattr(self.step, 'final', e.control.value)
                        ),
            ft.TextField(label='Cleanup', dense=True, multiline=True,
                         min_lines=2, max_lines=20, value=self.step.cleanup_text,
                         on_change=lambda e: setattr(self.step, 'cleanup_text', e.control.value)),
            ft.Row([ft.TextField(label='Prepare hours',
                                 dense=True,
                                 width=200,
                                 value=self.step.prepare_hours,
                                 text_align=ft.TextAlign.RIGHT,
                                 on_change=lambda e: setattr(self.step,'prepare_hours',e.control.value)),
                    ft.TextField(label='Cooldown hours',
                                 dense=True,
                                 value=self.step.cooldown_hours,
                                 width=200,
                                 text_align=ft.TextAlign.RIGHT,
                                 on_change=lambda e: setattr(self.step,'cooldown_hours',e.control.value)),
                    ]),
        ]
        return ft.Container(expand=True,
                            content=ft.Column(expand=True,
                                              scroll=ft.ScrollMode.ALWAYS,
                                              width=800,
                                              controls=control_list))

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
        self.mfgdocsapp.load_mainmarkdown_step(self.step.key)

    def parent_search_update(self):
        if self.mfgdocsapp.ctrl['panel_searchresults_container'].visible:
            self.mfgdocsapp.search(None)

    def dialog_preview(self, e):
        del e
        self.parent_search_update()
        self.parent_markdown_update()
        self.mfgdocsapp.page.update()
