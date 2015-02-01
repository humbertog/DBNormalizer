__author__ = 'humberto'

from DBNormalizer.view.View import *
from DBNormalizer.model.Model import *
from DBNormalizer.view.AC_topWindow import *


class Controller():
    def __init__(self):
        self.model = Model()

        self.root = Tk()
        self.root.geometry("1000x600+300+300")
        self.root.title("Super DB Normalizer")
        self.view = View(self.root)

        #
        self.current_relation = None

        self.view.side_panel.relation_tree.tree.bind("<Double-1>", self.select_relation)
        self.view.connection_panel.connect_button.bind("<Button>", self.get_database_metadata)
        self.view.right_panel.frame_four_t.subFrame4.\
            buttons_frame.button_normalization.bind("<Button>", self.compute_decomposed_relations)
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_buttons_1.button_remove.bind("<Button>",
                                                                                                       self.remove_fd)
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_buttons_1.\
            button_save.bind("<Button>", self.save_relation)
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_buttons_1.\
            button_add.bind("<Button>", self.add_fd)

        # Attribute Closure button
        self.view.right_panel.frame_three_t.attributeButton.button_attribute_closure.\
            bind("<Button>", self.get_attr_closure)


        # Attribute Closure


        #
        self.show_defaults()



    def show_defaults(self):
        self.view.connection_panel.host.insert(0, self.model.host)
        #TODO remember to change this
        self.view.connection_panel.username.insert(0, 'Gabriela')
        self.view.connection_panel.database.insert(0, 'Test')

    def run(self):
        self.root.mainloop()

    def add_fd(self, event):
        inputDialog = MyDialog(self.root)
        self.root.wait_window(inputDialog.top)
  #      print(inputDialog)
        if inputDialog.fd is not None:
            self.model.add_fd(inputDialog.fd, self.current_relation)

    def remove_fd(self, event):
        fd_idx = self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_table.curselection()
        if len(fd_idx) != 0:
            fd = self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_table.selection_get()
            removed = self.model.remove_fd_idx(self.current_relation, fd_idx[0])
            print(removed)
            self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_table.delete(fd_idx[0])

    def save_relation(self, event):
        name = self.current_relation
        self.model.update_relation(name)
        self.update_right_panel(name)

    def get_attr_closure(self, event):
        inputDialog2 = MyDialog_AC(self.root)
        print(inputDialog2.attr)
        self.root.wait_window(inputDialog2.top)
 #       print(inputDialog2)
        if inputDialog2.attr is not None:
            self.view.right_panel.frame_three_t.subFrame3_2.attr_closure_list.delete(0,END)
            closure = self.model.get_attr_closure(inputDialog2.attr, self.current_relation)
            print(closure)
            for attribute in closure:
                self.view.right_panel.frame_three_t.subFrame3_2.attr_closure_list.insert(END,attribute)

    def update_violations(self):
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.delete(1.0, END)

        nf2 = self.model.get_violation(self.current_relation, nf='2NF')
        nf3 = self.model.get_violation(self.current_relation, nf='3NF')
        bcnf = self.model.get_violation(self.current_relation, nf='BCNF')

        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.insert(INSERT, '2NF: \n')
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.insert(INSERT, str(nf2))
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.insert(INSERT, "\n3NF: \n")
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.insert(INSERT, str(nf3))
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.insert(INSERT, "\nBCNF: \n")
        self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab3.text_box.insert(INSERT, str(bcnf))

    def add_relation(self, parent, relation, original=True):
        if original:
            val = ['relation', 'original', relation.name]
        else:
            val = ['relation', 'decomposition', relation.name]

        par = self.view.side_panel.relation_tree.tree.insert(parent, "end", iid=relation.name, text=relation.name,
                                                             value=val)
        for attr in relation.attributes:
            self.view.side_panel.relation_tree.tree.insert(par, "end",  text=attr, value=['column', 'attr', attr])

    def populate_from_relation_dict(self, parent, rel_dic):
        for rel in rel_dic.keys():
            self.add_relation(parent, rel_dic[rel])

    def delete_decomposition(self):
        original_names = self.model.get_original_relations_names()
        for name in original_names:
            tree_values = self.view.side_panel.relation_tree.tree.get_children(name)
            for item in tree_values:
                item_values = self.view.side_panel.relation_tree.tree.item(item)
                if item_values['values'][1] == 'decomposition':
                    self.view.side_panel.relation_tree.tree.delete(item)

    def compute_decomposed_relations(self, event, nf='BCNF'):
        self.delete_decomposition()
        if nf == '3NF':
            self.model.compute_normalization_proposal_3NF()
        else:
            self.model.compute_normalization_proposal_BCNF()
        #
        print(self.model.relations)
        relation_names = self.model.get_original_relations_names()
        for name in relation_names:
            decomposition_names = self.model.get_decomposition_names(name)
            for dec_name in decomposition_names:
                rel = self.model.get_relation(dec_name)
                self.add_relation(name, rel, original=False)

    def clear_right_panel(self):
        #
        self.view.right_panel.frame_one_t.subFrame1.var_name.set("")
        self.view.right_panel.frame_one_t.subFrame1.var_nf.set("")

    # Update right panel (relation info
    def select_relation(self, event):
        item = self.view.side_panel.relation_tree.tree.selection()[0]
        item_values = self.view.side_panel.relation_tree.tree.item(item)
        kind = item_values['values'][0]
        name = item_values['text']
        if kind == 'relation':
            self.current_relation = name
            self.update_right_panel(name)


    # def update_attribute_closure(self, attr, name):
    #    # self.view.right_panel.frame_three_t.subFrame3_2.attr_closure_list.set()
    #    # self.view.right_panel.frame_three_t.subFrame3_2.attr_closure_list.delete(0,END)
    #     closure = self.model.get_attr_closure(self.inputDialog2.attr, self.name)
    #     if len(closure) != 0:
    #         for a in closure:
    #             self.view.right_panel.frame_three_t.subFrame3_2.attr_closure_list.insert(END, a)

    def update_right_panel(self, name):
            self.clear_right_panel()
            self.view.right_panel.frame_one_t.subFrame1.var_name.set(name)
            nf = self.model.get_NF(name)
            print(nf)
            self.view.right_panel.frame_one_t.subFrame1.var_nf.set(nf)

            # Candidate keys:
            self.view.right_panel.frame_three_t.subFrame3.keys_list.delete(0,END)
            keys = self.model.get_candidate_keys(name)
            if len(keys) != 0:
                for key in keys:
                    self.view.right_panel.frame_three_t.subFrame3.keys_list.insert(END, list(key))

            # Canonical cover:
            self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab2.cover_table.delete(0, END)
            cc = self.model.get_canonical_cover(name)
            if cc is not None:
                for fd in cc:
                    self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab2.cover_table.insert(END, fd)

            # FDs:
            self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_table.delete(0,END)
            fds = self.model.get_fds(name)
            if len(fds) != 0:
                for fd in fds:
                    self.view.right_panel.frame_two_t.subFrame2.fds_notebook.tab1.fds_table.insert(END,fd)

            # FDS violations:
            self.update_violations()





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


