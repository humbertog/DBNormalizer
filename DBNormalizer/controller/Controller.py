__author__ = 'humberto'

from DBNormalizer.view.View import *
from DBNormalizer.model.Model import *


class Controller():
    def __init__(self):
        self.model = Model()

        self.root = Tk()
        self.root.geometry("800x500+300+300")
        self.view = View(self.root)

        #
        self.view.side_panel.relation_tree.tree.bind("<Double-1>", self.select_relation)
        self.view.connection_panel.connect_button.bind("<Button>", self.get_database_metadata)

        #
        self.show_defaults()

    def show_defaults(self):
        self.view.connection_panel.host.insert(0, self.model.host)
        #self.view.connection_panel.username.insert(0, 'humberto')
        #self.view.connection_panel.database.insert(0, 'dbnormalizer_test')

    def run(self):
        self.root.mainloop()

    def add_relation(self, parent, relation):
        par = self.view.side_panel.relation_tree.tree.insert(parent, "end", iid=relation.name, text=relation.name,
                                                             value=['relation', relation.name])
        for attr in relation.attributes:
            self.view.side_panel.relation_tree.tree.insert(par, "end",  text=attr, value=['column', attr])

    def populate_from_relation_dict(self, parent, rel_dic):
        for rel in rel_dic.keys():
            self.add_relation(parent, rel_dic[rel])

    def select_relation(self, event):
        item = self.view.side_panel.relation_tree.tree.selection()[0]
        item_values = self.view.side_panel.relation_tree.tree.item(item)
        kind = item_values['values'][0]
        name = item_values['text']
        if kind == 'relation':
            print(self.model.relations[name].fds)

#        print("you clicked on", self.view.side_panel.relation_tree.tree.item(item))

    def get_database_metadata(self, event):
        host = self.view.connection_panel.host.get()
        port = self.view.connection_panel.port.get()
        username = self.view.connection_panel.username.get()
        password = self.view.connection_panel.password.get()
        database = self.view.connection_panel.database.get()

        self.model.set_db_connection_params(username, password, host, database, port)

        self.model.get_metadata()
        self.model.get_schema()
        self.model.append_fds()

        self.view.side_panel.relation_tree.delete_tree()
        self.view.side_panel.relation_tree.tree.insert('', "end", text='')
        self.populate_from_relation_dict('', self.model.relations)


        #


