"""Contains Markdown rendering functions."""
import itertools

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
# {step.key} {step.name} [:pencil2:](click://step_edit/{step.pk})
 - :busts_in_silhouette: {self.lookup_single_item(step.company, s.cache_companies.data)} :round_pushpin: {self.lookup_single_item(step.location, s.cache_locations.data)} :clock1: {step.prepare_hours} :clock2: {step.cooldown_hours}
| Input [:pencil2:](click://step_edit_inputparts/{step.pk})| Output [:pencil2:](click://step_edit_outputparts/{step.pk})| Roles [:pencil2:](click://step_edit_roles/{step.pk})| Actions [:pencil2:](click://step_edit_actions/{step.pk})| Machines [:pencil2:](click://step_edit_machines/{step.pk})| Tools [:pencil2:](click://step_edit_tools/{step.pk})| Consumables [:pencil2:](click://step_edit_consumables/{step.pk})|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
{self.multitable(step,step.inputparts, s.cache_parts.data,
                 step.outputparts, s.cache_parts.data,
                 step.roles, s.cache_roles.data,
                 step.actions, s.cache_actions.data,
                 step.machines, s.cache_machines.data,
                 step.tools, s.cache_tools.data,
                 step.consumables, s.cache_consumables.data)}
{'## Prepare' if len(step.prepare_text.strip()) > 0 else ''}
{'## Prepare' if len(step.prepare_text.strip()) > 0 else ''}
{step.prepare_text}

{'## Description' if len(step.description.strip()) > 0 else ''}
{step.description}

{'## Acceptance criteria' if len(step.acceptance.strip()) > 0 else ''}
{step.acceptance}

{'## Cleanup' if len(step.cleanup_text.strip()) > 0 else ''}
{step.cleanup_text}

{'## Depends on ' if len(step.start_after) > 0 else ''}

{self.list_items(step.start_after, s.cache_steps.data)}

{'## Parallel with ' if len(step.start_after_start) > 0 else ''}

{self.list_items(step.start_after_start, s.cache_steps.data)}


        '''
        return md

    def lookup_single_item(self, key, data: dict) -> str:
        return f"{key} {data[key].name if key in data else 'MISSING'}"

    def list_items(self, items: dict, data: dict, separator=', ') -> str:
        return separator.join(list(map(lambda key: f"{key} {data[key].name if key in data else 'MISSING'}",
                                       items.keys())))

    def list_amounts(self, items: dict, data: dict, separator=', ', unit='', multiplicator=' :heavy_multiplication_x: ',
                     missing_marker=':triangular_flag_on_post: MISSING') -> str:
        return separator.join(list(map(
            lambda
                key: f"{key} {data[key].name + multiplicator + str(items[key]) + ' ' + unit if key in data else missing_marker}",
            items.keys())))

    def list_amounts_pre(self, items: dict, data: dict, separator=', ', unit='',
                         multiplicator=':heavy_multiplication_x:',
                         missing_marker=':triangular_flag_on_post: MISSING ') -> str:
        unit_with_space = (unit + ' ' + multiplicator + ' ' if unit != '' else multiplicator + ' ')
        return separator.join(list(map(
            lambda key: f"{str(items[key]) + ' ' + unit_with_space + key + ' ' + data[key].name}" if key in data
            else missing_marker + str(items[key]) + ' ' + multiplicator + ' ' + key, items.keys())))

    def multitable(self, step:Step, ipart, ipartdata, opart, opartdata, roles, rolesdata, actions, actionsdata, machines,
                   machinesdata, tools, toolsdata, consumables, consumablesdata) -> str:
        ipartlist = self.list_from_itemlist_and_data(ipart, ipartdata)
        opartlist = self.list_from_itemlist_and_data(opart, opartdata, ':heavy_check_mark:' if step.final else '('+step.key+')')
        roleslist = self.list_from_itemlist_and_data(roles, rolesdata)
        actionslist = self.list_from_itemlist_and_data(actions, actionsdata)
        machineslist = self.list_from_itemlist_and_data(machines, machinesdata)
        toolslist = self.list_from_itemlist_and_data(tools, toolsdata)
        consumableslist = self.list_from_itemlist_and_data(consumables, consumablesdata)

        table = ''
        for (ipart, opart, role, action, machine, tool, consumable) in itertools.zip_longest(ipartlist, opartlist,
                                                                                             roleslist, actionslist,
                                                                                             machineslist, toolslist,
                                                                                             consumableslist,
                                                                                             fillvalue=''):
            table += '| ' + ipart + ' | ' + opart + ' | ' + role + ' | ' + action + ' | ' + machine + ' | ' + tool + ' | ' + consumable + ' | \n'
        return table

    def list_from_itemlist_and_data(self, itemdict: dict, data: dict, append: str = '') -> list:
        lst = []
        print(itemdict)
        for k, v in itemdict.items():
            item = data[k]
            lst.append(f"{v} {item.unit} x {k}{' '+append if append != '' else ''} - {item.name}")
        return lst
