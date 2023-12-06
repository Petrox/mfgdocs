"""Builds and handles the list of resources in a Step.

Use the dialog property to access the dialog control.
"""
import copy

import flet as ft
from model import Step
from ingredidentlisteditor import IngredientListEditor


class StepResourceListEditor():
    """Builds and handles the list of resources in a Step.
    """
    dialog: ft.AlertDialog
    original_step: dict

    def __init__(self, mfgdocsapp: 'MFGDocsApp', step: Step, itemlist: dict, resource_type: str, title: str, is_inputpart: bool = False):
        self.is_inputpart = is_inputpart
        self.itemlist = itemlist
        self.title = title
        self.resource_type = resource_type
        self.mfgdocsapp = mfgdocsapp
        self.step = step
        self.original_step = copy.deepcopy(step.to_dict())
        self.dialog = ft.AlertDialog(modal=False)
        self.dialog.title = ft.Text(title)
        self.dialog.content = self.build()
        self.dialog.actions = [ft.TextButton('Cancel', on_click=self.dialog_cancel),
                               ft.TextButton('Save', on_click=self.dialog_save)]
        self.dialog.actions_alignment = 'end'
        self.dialog.shape = ft.BeveledRectangleBorder()
        self.dialog.visible = True

    def build(self) -> ft.Control: # pylint: disable=too-many-locals
        """Builds the dialog content."""
        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True, scroll=ft.ScrollMode.ALWAYS, width=800,
                controls=[
                    IngredientListEditor(
                        '',
                        self.itemlist,
                        resource_type=self.resource_type,
                        storage=self.mfgdocsapp.storage,
                        is_inputpart=self.is_inputpart
                        )
                ]
                )
            )

    def dialog_cancel(self, e):
        """Closes the dialog without saving changes."""
        del e
        self.dialog.open = False
        self.step.from_dict(self.original_step)
        self.parent_search_update()
        self.parent_markdown_update()
        self.mfgdocsapp.page.update()

    def dialog_save(self, e):
        """Closes the dialog and saves changes."""
        del e
        self.mfgdocsapp.storage.save_resources()
        self.dialog.open = False
        self.parent_search_update()
        self.parent_markdown_update()
        self.mfgdocsapp.page.update()

    def parent_markdown_update(self):
        """Updates the markdown in the main view."""
        self.mfgdocsapp.load_mainmarkdown_step(self.step.key)

    def parent_search_update(self):
        """Updates the search results in the main view."""
        if self.mfgdocsapp.ctrl['panel_searchresults_container'].visible:
            self.mfgdocsapp.search(None)
