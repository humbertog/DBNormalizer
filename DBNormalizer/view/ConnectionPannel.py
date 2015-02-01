__author__ = 'humberto'

from tkinter import *
from tkinter import ttk

class ConnectionPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.initialize()

    def initialize(self):

        self.grid()

        host_label = Label(self, text="Host", anchor="w")
        port_label = Label(self, text="Port", anchor="w")
        username_label = Label(self, text="Username", anchor="w")
        password_label = Label(self, text="Password", anchor="w")
        database_label = Label(self, text="Database", anchor="w")

        self.host = Entry(self)
        self.port = Entry(self)
        self.username = Entry(self)
        self.password= Entry(self)
        self.database = Entry(self)

        self.host.grid(column=1,row=1,sticky='EW')
        self.port.grid(column=1,row=2,sticky='EW')
        self.username.grid(column=3,row=1,sticky='EW')
        self.password.grid(column=3,row=2,sticky='EW')
        self.database.grid(column=5,row=1,sticky='EW')

        host_label.grid(column=0,row=1,sticky='EW')
        port_label.grid(column=0,row=2,sticky='EW')
        username_label.grid(column=2,row=1,sticky='EW')
        password_label.grid(column=2,row=2,sticky='EW')
        database_label.grid(column=4,row=1,sticky='EW')

        self.connect_button = Button(self, text="Connect DB")
        #self.cancel_button = Button(self,text="Cancel", command=self.destroy)

        self.connect_button.grid(column=4,row=2)
        #self.cancel_button.grid(column=0,row=6)

        self.sql_output_button = Button(self, text="Export DDL")
        self.sql_output_button.grid(column=5,row=2,sticky='EW')