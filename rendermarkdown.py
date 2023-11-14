"""Contains Markdown rendering functions."""
from model import Part, Step


class RenderMarkdown:
    """This class renders entities to markdown."""

    def __init__(self, mfgdocsapp):
        self.mfgdocsapp = mfgdocsapp
        self.storage = mfgdocsapp.storage

    def render_part(self, part: Part) -> str:
        """Renders a part to markdown.

        :param part: The part to render.
        :return: The rendered markdown.
        """
        md = f'''# {part.key} {part.name}'''

        return md

    def render_step(self, step: Step) -> str:
        """Renders a step to markdown.

        :param step: The step to render.
        :return: The rendered markdown.
        """
        s = self.mfgdocsapp.storage
        md = f'''
# {step.key} {step.name} To produce: {self.list_amounts(step.outputparts, s.cache_parts.data)}
 - By: {self.list_amounts(step.roles, s.cache_roles.data)}
 - At: {self.list_items(step.location, s.cache_locations.data)}

| Input | Machines | Tools | Actions | Consumables |
| :---: | :---: | :---: | :---: | :---: |
| {self.list_amounts_pre(step.inputparts, s.cache_parts.data, separator='  ')} | {
        self.list_amounts_pre(step.machines, s.cache_machines.data, separator='  ')} | {
        self.list_amounts_pre(step.tools, s.cache_tools.data, separator='  ')} | {
        self.list_amounts_pre(step.actions, s.cache_actions.data, separator='  ', unit='h')} | {
        self.list_amounts_pre(step.consumables, s.cache_consumables.data, separator='  ')} |

{step.description}

{'## Acceptance criteria' if len(step.acceptance.strip()) > 0 else ''}
{step.acceptance}

 - Start after: {self.list_items(step.start_after, s.cache_steps.data)}
 - Start after start: {self.list_items(step.start_after_start, s.cache_steps.data)}


        '''
        return md

    def list_items(self, items: dict, data: dict, separator=', ') -> str:
        return separator.join(list(map(lambda key: f"{key} {data[key].name if key in data else 'MISSING'}",
                                       items.keys())))

    def list_amounts(self, items: dict, data: dict, separator=', ', unit='') -> str:
        return separator.join(list(map(
            lambda key: f"{key} {data[key].name + ' x ' + str(items[key]) + ' ' + unit if key in data else 'MISSING'}",
            items.keys())))

    def list_amounts_pre(self, items: dict, data: dict, separator=', ', unit='') -> str:

        unit_with_space = (unit + ' x ' if unit != '' else 'x ')
        return separator.join(list(map(
            lambda key: f"{str(items[key]) + ' ' + unit_with_space + key + ' ' + data[key].name}" if key in data
            else 'MISSING: ' + str(items[key]) + ' x ' + key,items.keys())))