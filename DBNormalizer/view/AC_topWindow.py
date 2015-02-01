__author__ = 'Nantes'


from tkinter import *

class MyDialog_AC:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.top.geometry("300x120+150+100")
        self.top.resizable(0,0)

        self.parent = parent
        self.myLabel = Label(top, text='Add attributes')
        self.myLabel.pack()

        self.myEntryBox = Entry(top)
        self.myEntryBox.pack(side=TOP, expand=1, fill=X)


        self.mySubmitButton_ac = Button(top, text='Add', command=self.send)
        self.mySubmitButton_ac.pack(side=LEFT, expand= 1)

        self.cancel_button = Button(top, text='Cancel', command=self.cancel)
        self.cancel_button.pack(side=LEFT, expand=1)

        self.attr = None

        self.top.transient(self.parent)
        self.top.grab_set()

        #self.parent.wait_window(top)

    def send(self):
        self.attr = {'attr':self.myEntryBox.get()}
        self.top.destroy()

    def cancel(self):
        self.top.destroy()
