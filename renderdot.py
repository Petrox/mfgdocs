"""
Handles rendering the dataset with graphviz

"""
import os

import graphviz
from graphviz import Digraph

from model import Step, Part


class RenderDot:
    """Generates dot graph content and renders it to a file."""

    def __init__(self, mfgdocsapp: 'MFGDocsApp'):
        self.mfgdocsapp = mfgdocsapp
        self.storage = mfgdocsapp.storage

    def render_bom_to_file(self, options=None, extension='png'):
        if options is None:
            options = {}
        dg = graphviz.Digraph(encoding='utf-8', name='Manufacturing Document')
        dg.attr(rankdir='TD', size='8,5', dpi='600')
        edges = []
        for i in self.storage.cache_parts.data.keys():
            part = self.storage.cache_parts.data[i]
            self.dot_render_part_compact(dg, part)
            # dg.node(i, part.name)
            for bom in part.bom:
                edges.append([bom, i])
        for e in edges:
            dg.edge(e[0], e[1])
        dg.render('tempfiles/dg.dot', view=True, format=extension)

    def render_steps_to_file(self, options=None, extension='png'):
        if options is None:
            options = {}
        dg = graphviz.Digraph(encoding='utf-8', name='Manufacturing Document')
        dg.attr(rankdir='TD', size='15,15', dpi='300')
        edges = {}
        nodes = {}
        for stepkey, step in self.storage.cache_steps.data.items():
            nodes[stepkey] = True
            self.dot_render_step_compact(dg, step)
            for partkey, amount in step.inputparts.items():
                only_partkey, only_stepkey = Part.extract_stepkey(partkey)
                part = self.storage.cache_parts.data[only_partkey]
                if partkey not in nodes:
                    nodes[partkey] = True
                    self.dot_render_part_compact(dg, part, partkey)
                edgekey = f'{partkey}-in-{stepkey}'
                edges[edgekey] = {'from': partkey, 'to': stepkey, 'amount': amount}
                dg.edge(partkey, stepkey, label=f'{amount} {part.unit}')

            for only_partkey, amount in step.outputparts.items():

                if not step.final:
                    partkey = f'{only_partkey}({stepkey})'
                else:
                    partkey = only_partkey
                print(f'dot output partkey from {stepkey}: {partkey}')
                part = self.storage.cache_parts.data[only_partkey]
                if partkey not in nodes:
                    nodes[partkey] = True
                    self.dot_render_part_compact(dg, part, partkey)
                edgekey = f'{stepkey}-out-{partkey}'
                edges[edgekey] = {'from': stepkey, 'to': partkey, 'amount': amount}
                dg.edge(stepkey, partkey, label=f'{amount} {part.unit}')

        dotfilename = 'assets/generated/overview.dot'
        try:
            os.remove(dotfilename)
            os.remove(dotfilename + '.png')
        except FileNotFoundError:
            pass
        dg.render(dotfilename, format=extension, view=False, overwrite_source=True)

    def dot_render_part_compact(self, dg: Digraph, part: Part, displaykey=None):
        dg.attr('node', shape='plain', style='filled', fillcolor='lightgrey', fontname='Courier New', fontsize='15',
                fixedsize='false')

        dg.node(displaykey, f'''<
        <TABLE BORDER="1" CELLBORDER="0" COLOR="palegreen" CELLSPACING="0" CELLPADDING="4">
          <TR>
            <TD COLOR="palegreen">{displaykey}</TD>
          </TR><TR>
            <TD COLOR="palegreen">{part.name}</TD>
          </TR>
        </TABLE>>''')

    def dot_render_step_compact(self, dg: Digraph, step: Step):
        dg.attr('node', shape='plain', style='filled', fillcolor='lightgrey', fontname='Courier New', fontsize='15',
                fixedsize='false')

        dg.node(step.key, f'''<
        <TABLE BORDER="1" CELLBORDER="0" BGCOLOR="LIGHTBLUE" CELLSPACING="0" CELLPADDING="4">
          <TR>
            <TD COLOR="BLUE">{step.key}</TD>
          </TR><TR>
            <TD COLOR="BLUE">{step.name}</TD>
          </TR>
        </TABLE>>''')

#         dg.node(part.key, f'''<
# <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
#   <TR>
#     <TD ROWSPAN="3">{part.key}</TD>
#     <TD COLSPAN="3">{part.name}</TD>
#     <TD ROWSPAN="3">g</TD>
#     <TD ROWSPAN="3">h</TD>
#   </TR>
#   <TR>
#     <TD>c</TD>
#     <TD PORT="here">d</TD>
#     <TD>e</TD>
#   </TR>
#   <TR>
#     <TD COLSPAN="3">f</TD>
#   </TR>
# </TABLE>>''')
# dg.node(part.key, part.name)
