__author__ = 'Nantes'

from tkinter import *

class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.top.geometry("400x150+100+50")
        self.top.resizable(0,0)
        self.parent = parent
        self.myLabel = Label(top, text='Add functional dependency')
        self.myLabel.pack()

        self.myEntryBox_left = Entry(top)
        self.myEntryBox_left.pack(expand=1, fill=X)

        self.myEntryBox_right = Entry(top)
        self.myEntryBox_right.pack(expand=1, fill=X)

        self.mySubmitButton = Button(top, text='Add', command=self.send)
        self.mySubmitButton.pack()

        self.cancel_button = Button(top, text='Cancel', command=self.cancel)
        self.cancel_button.pack()

        self.fd = None

        self.top.transient(self.parent)
        self.top.grab_set()
        #self.parent.wait_window(top)

    def send(self):
        self.fd = {'lhs':self.myEntryBox_left.get(), 'rhs':self.myEntryBox_right.get()}
        self.top.destroy()

    def cancel(self):

        self.top.destroy()
