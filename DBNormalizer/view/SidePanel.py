__author__ = 'humberto'

from tkinter import *
from tkinter import ttk


class SidePanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.tree_buttons = RelationTreeButtons(self)
        self.tree_buttons.pack(side=TOP)

        self.relation_tree = RelationTree(self)
        self.relation_tree.pack(anchor=NW, expand=1, fill=BOTH)


        #self.add_relation_button = Button(self, text="Add Relation")
        #self.add_relation_button.pack(side=BOTTOM)

        #self.remove_relation_button = Button(self, text="Remove")
        #self.remove_relation_button.pack(side=BOTTOM)
        #self.tree_buttons.pack(side=BOTTOM)


class RelationTreeButtons(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #        self.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.frame = ttk.Frame(self)

        self.add_relation_button = ttk.Button(self, text="Add Relation")
        self.add_relation_button.pack(side=LEFT)

        self.add_attribute_button = ttk.Button(self, text='Add Attribute')
        self.add_attribute_button.pack(side=LEFT)

        self.remove_relation_button = ttk.Button(self, text="Remove")
        self.remove_relation_button.pack(side=LEFT)


class RelationTree(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #        self.pack(anchor=W, expand=1, fill=Y)
        self.parent = parent
        self.tree = ttk.Treeview(self)
        # self.tree.bind("<Double-1>", self.on_double_click)

        ysb = ttk.Scrollbar(self.tree, orient=VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree, orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # setup column headings
        self.tree.heading('#0', text='Schema', anchor=NW)

        ysb.pack(side=RIGHT, fill=Y)
        xsb.pack(side=BOTTOM, fill=X)
        self.tree.pack(expand=1, fill=BOTH)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def delete_tree(self):
        nodes = self.tree.get_children()
        for x in nodes:
            self.tree.delete(x)

