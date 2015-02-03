__author__ = 'Nantes'

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import font


class RightPanel(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)


        self.frame_one_t = frame_one(self)
        #self.frame_one_t.grid(column=1,row=2, sticky=(W,E))
        self.frame_one_t.pack(anchor=NW, expand=0, fill=X)

        self.frame_two_t = frame_two(self)
        #self.frame_two_t.grid(column=1,row=3, sticky=(W,E))
        self.frame_two_t.pack(anchor=NW, expand=1, fill=BOTH)

        self.frame_three_t = frame_three(self)
        #self.frame_three_t.grid(column=1,row=3, sticky=(W,E))
        self.frame_three_t.pack(anchor=NW, expand=0, fill=X)

        self.frame_four_t = frame_four(self)
        #self.frame_four_t.grid(column=1,row=3, sticky=(W,E))
        self.frame_four_t.pack(anchor=NW, expand=0, fill=X)

class frame_one(Frame):
    def __init__(self,parent):
        LabelFrame.__init__(self,parent, text="Table Name and Normal Form")
        #self.pack(anchor=NW, expand=1, fill=X)


        self.subFrame1 = subFrame(self)
        self.subFrame1.pack(anchor=NW, expand=0, fill=X)


class subFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        #self.pack(anchor=NW, expand=1, fill=X)
        # table_name = StringVar()
        # table_name_entry = ttk.Entry(self, width=7, textvariable=table_name)
        # table_name_entry.grid(column=1, row=1, sticky=(W, E))

        fonts = font.Font(size=12, weight='bold')
        self.table_label = Label(self, text="Relation Name: ")
        self.table_label.pack(anchor=NW)
        self.var_name = StringVar()
        self.table_name = ttk.Label(self, textvariable=self.var_name, font=fonts)
        self.table_name.pack(anchor=NW)

        self.nf_label = Label(self, text="Normal Form: ")
        self.nf_label.pack(anchor=NW)
        self.var_nf = StringVar()
        self.normal_form = ttk.Label(self, textvariable=self.var_nf, font=fonts)
        self.normal_form.pack(anchor=NW)

        #self.table_label.grid(column=0, row=0)
        #self.nf_label.grid(column=0, row=1)

        #self.table_name.grid(column=1, row=0)
        #self.normal_form.grid(column=1, row=1)

class TableName(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.table_name_entry = ttk.Label(self, text="")
        #self.table_name_entry.grid(column=1, row=1, sticky=(NW))

class NormalForm(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.normal_form_entry = ttk.Label(self, text="")
        #self.normal_form_entry.grid(column=1, row=1, sticky=(NW))

class frame_two(Frame):
    def __init__(self,parent):
        LabelFrame.__init__(self,parent, text="FDs and Table Information", width=100)
        #self.pack(anchor=N, expand=1, fill=BOTH)

        self.subFrame2 = subFrame2(self)
        self.subFrame2.pack(anchor=N, expand=1, fill=BOTH)

class subFrame2(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        #self.pack(anchor=NW, expand=1, fill=BOTH)
        # table_name = StringVar()
        # table_name_entry = ttk.Entry(self, width=7, textvariable=table_name)
        # table_name_entry.grid(column=1, row=1, sticky=(W, E))
        self.fds_notebook = FDS_notebook(self)
        self.fds_notebook.pack(anchor=N, expand=1, fill=BOTH)


class FDS_notebook(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)
        self.n = ttk.Notebook(self)
        self.tab1 = FDS_tab1(None)
        self.n.add(self.tab1, text='FDs', sticky=N+E+S+W)
        self.tab2 = FDS_tab2(None)
        self.n.add(self.tab2, text='Minimal Cover', sticky=N+E+S+W)
        self.tab3=FDS_tab3(None)
        self.n.add(self.tab3, text='NF Violations', sticky=N+E+S+W)
        self.tab4=FDS_tab4(None)
        self.n.add(self.tab4, text='Table Information', sticky=N+E+S+W)
        #self.n.grid(sticky=N)
        self.n.pack(expand=1, fill=BOTH)

class FDS_tab1(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)

        self.fds_table = Listbox(self)
        self.fds_table.pack(expand=1, fill=BOTH)

        self.fds_buttons_1 = FDS_tab1_buttons(self)
        self.fds_buttons_1.pack(fill=BOTH, side=BOTTOM)

        ysb = ttk.Scrollbar(self.fds_table, orient=VERTICAL, command=self.fds_table.yview)
        xsb = ttk.Scrollbar(self.fds_table,orient=HORIZONTAL, command=self.fds_table.xview)
        self.fds_table['yscroll'] = ysb.set
        self.fds_table['xscroll'] = xsb.set

        self.fds_table.pack(expand=1, fill=BOTH)
        ysb.pack(side=RIGHT, fill=Y)
        xsb.pack(side=BOTTOM, fill=X)


class FDS_tab1_buttons(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.tab1_frame = ttk.Frame(self)
        self.tab1_frame.pack(side= BOTTOM)

        self.button_remove = ttk.Button(self.tab1_frame, text="Remove")
        self.button_remove.pack(side=LEFT)
        self.button_add = ttk.Button(self.tab1_frame, text="Add")
        self.button_add.pack(side=LEFT)
        self.button_save = ttk.Button(self.tab1_frame, text="Save")
        self.button_save.pack(side=LEFT)


class FDS_tab2(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)

        self.cover_table = Listbox(self)
        #self.cover_table.pack(expand=1, fill=BOTH)

        ysb = ttk.Scrollbar(self.cover_table, orient=VERTICAL, command=self.cover_table.yview)
        xsb = ttk.Scrollbar(self.cover_table,orient=HORIZONTAL, command=self.cover_table.xview)
        self.cover_table['yscroll'] = ysb.set
        self.cover_table['xscroll'] = xsb.set

        self.cover_table.pack(expand=1, fill=BOTH)
        ysb.pack(side=RIGHT, fill=Y)
        xsb.pack(side=BOTTOM, fill=X)


class FDS_tab3(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)

        self.text_box = Text(self, height=10)
        self.text_box.pack(expand=1, fill=BOTH)

        ysb = ttk.Scrollbar(self.text_box, orient=VERTICAL, command=self.text_box.yview)
        self.text_box['yscroll'] = ysb.set
        ysb.pack(side=RIGHT, fill=Y)


class FDS_tab4(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)

        self.text_box = Text(self, height=10)
        self.text_box.pack(expand=1, fill=BOTH)

        ysb = ttk.Scrollbar(self.text_box, orient=VERTICAL, command=self.text_box.yview)
        self.text_box['yscroll'] = ysb.set
        ysb.pack(side=RIGHT, fill=Y)


class Table_info_label(Frame):
    def __init__(self, parent):
        Label.__init__(self, parent, text= "table name, attribute, etc")
#        table_name = StringVar()
#        table_name_entry = ttk.Entry(self,  textvariable=table_name)

class frame_three(Frame):
    def __init__(self,parent):
        LabelFrame.__init__(self,parent, text="Candidate Keys and attribute closure")
        #self.pack(anchor=N, expand=1, fill=BOTH)

        self.subFrame3 = subFrame3(self)
        self.subFrame3.pack(side=LEFT, expand=1, fill=X)

        self.subFrame3_2 = subFrame3_2(self)
        self.subFrame3_2.pack(side=LEFT, expand=1, fill=X)

        self.attributeButton = attribute_closure_button(self)
        self.attributeButton.pack(side=LEFT, expand=1,fill=X)


class subFrame3(Frame):
    def __init__(self,parent):
        LabelFrame.__init__(self, parent, text="Candidate Keys")
        #self.pack(anchor=NW, expand=1, fill=BOTH)
        # table_name = StringVar()
        # table_name_entry = ttk.Entry(self, width=7, textvariable=table_name)
        # table_name_entry.grid(column=1, row=1, sticky=(W, E))
        self.keys_list = Listbox(self, height=7)


        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.keys_list.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.keys_list.xview)
        self.keys_list['yscroll'] = ysb.set
        self.keys_list['xscroll'] = xsb.set
        self.keys_list.grid(in_=self, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=self, row=0, column=1, sticky=NS)
        xsb.grid(in_=self, row=1, column=0, sticky=EW)
        #self.keys_list.pack(anchor=NW, fill=X)


class subFrame3_2(Frame):
    def __init__(self,parent):
        LabelFrame.__init__(self,parent, text="Attribute Closure")
        self.attr_closure_list = Listbox(self, height=7)

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.attr_closure_list.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.attr_closure_list.xview)
        self.attr_closure_list['yscroll'] = ysb.set
        self.attr_closure_list['xscroll'] = xsb.set
        self.attr_closure_list.grid(in_=self, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=self, row=0, column=1, sticky=NS)
        xsb.grid(in_=self, row=1, column=0, sticky=EW)


class attribute_closure_button(Frame):
       def __init__(self,parent):
        Frame.__init__(self,parent)

        self.button_attribute_closure = ttk.Button(self, text="Attribute Closure")
        self.button_attribute_closure.pack(side=LEFT)


class frame_four(Frame):
    def __init__(self,parent):
        LabelFrame.__init__(self,parent)
        #self.pack(anchor=N, expand=1, fill=BOTH)


        self.subFrame4 = subFrame4(self)
        self.subFrame4.pack(anchor=NW, expand=0)


class subFrame4(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        #self.pack(anchor=NW, expand=1, fill=BOTH)
        # table_name = StringVar()
        # table_name_entry = ttk.Entry(self, width=7, textvariable=table_name)
        # table_name_entry.grid(column=1, row=1, sticky=(W, E))
        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.pack(anchor=S)


class ButtonsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.button_normalization = ttk.Button(self, text="3NF Normalization")
        self.button_normalization.pack(side=LEFT)
        self.button_bcnf = ttk.Button(self, text="BCNF Normalization")
        self.button_bcnf.pack(side=LEFT)
