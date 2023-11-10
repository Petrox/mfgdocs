"""
Handles rendering the dataset with graphviz

"""
import graphviz

# from mfgdocsapp import MFGDocsApp
from graphviz import Digraph

from storage import Storage


class Render:
    def __init__(self, mfgdocsapp: 'MFGDocsApp', storage: Storage):
        self.mfgdocsapp = mfgdocsapp
        self.storage = storage

    def render(self, options=None):
        if options is None:
            options = {}
        dg = graphviz.Digraph(encoding='utf-8', name='Manufacturing Document')
        dg.attr(rankdir='TD', size='8,5', dpi='600')
        edges = []
        for i in self.storage.cache_parts.data.keys():
            part = self.storage.cache_parts.data[i]
            self.render_part_compact(dg, part)
            # dg.node(i, part.name)
            for bom in part.bom:
                edges.append([bom, i])
        for e in edges:
            dg.edge(e[0], e[1])
        dg.render('tempfiles/dg.dot', view=True, format='png')

    def render_part_compact(self, dg, part):
        """

        :type dg: Digraph
        """
        dg.attr('node', shape='plain', style='filled', fillcolor='lightgrey', fontname='Courier New', fontsize='40',
                fixedsize='false')

        dg.node(part.key, f'''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
          <TR>
            <TD BGCOLOR="BLUE" COLOR="WHITE">{part.key}</TD>
            <TD BGCOLOR="BLUE" COLOR="WHITE">{part.name}</TD>
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
        #dg.node(part.key, part.name)
