__author__ = 'humberto'

from DBNormalizer.view.ConnectionPannel import *
from DBNormalizer.view.SidePanel import *
from DBNormalizer.view.RightPanel import *
from DBNormalizer.view.FD_topWindow import *

class View():
    def __init__(self, parent):
        self.connection_panel = ConnectionPanel(parent)
        self.connection_panel.pack(anchor=NW, fill=X)

        self.side_panel = SidePanel(parent)
        self.side_panel.pack(side=LEFT, anchor=NW, expand=1, fill=BOTH)

        self.right_panel = RightPanel(parent)
        self.right_panel.pack(side=LEFT, anchor=NW, expand=1, fill=BOTH)

        #self.connection_panel.grid(row=0)
        #self.side_panel.grid(column=0, row=1)
        #self.right_panel.grid(column=1, row=1)
