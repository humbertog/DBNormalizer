__author__ = 'humberto'

from tkinter import *
from tkinter import ttk


class SidePanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        #self.connect_buttons = SidePanelButtons(self)
        #self.connect_buttons.pack(side=TOP)

        self.relation_tree = RelationTree(self)
        self.relation_tree.pack(anchor=NW, expand=1, fill=BOTH)

        self.tree_buttons = RelationTreeButtons(self)
        self.tree_buttons.pack(side=BOTTOM)


class RelationTreeButtons(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        #        self.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.button_view()

    def button_view(self):
        add_relation_button = Button(self, text="Add", command=self.add_relation)
        add_relation_button.pack(side=LEFT)
        remove_relation_button = Button(self, text="Remove", command=self.remove_relation)
        remove_relation_button.pack(side=LEFT)

    def add_relation(self):
        print("add relation")

    def remove_relation(self):
        print("remove relation")


class RelationTree(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #        self.pack(anchor=W, expand=1, fill=Y)
        self.parent = parent
        self.tree_view()

    def tree_view(self):
        self.tree = ttk.Treeview(self)
        # self.tree.bind("<Double-1>", self.on_double_click)

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # setup column headings
        self.tree.heading('#0', text='Schema', anchor=NW)
        self.tree.grid(in_=self, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=self, row=0, column=1, sticky=NS)
        xsb.grid(in_=self, row=1, column=0, sticky=EW)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def delete_tree(self):
        nodes = self.tree.get_children()
        for x in nodes:
            self.tree.delete(x)

