__author__ = 'Nantes'

from DBNormalizer.model.Relation import Relation
from DBNormalizer.model.SQLParser import get_table_partitions
from sqlalchemy import *
from sqlalchemy.schema import CreateTable
from DBNormalizer.model.FDependencyList import *
from DBNormalizer.model.Decomp import *


class Model():
    def __init__(self):
        self.username = None
        self.password = None
        self.host = 'localhost'
        self.database = None
        self.port = None
        self.engine = None

        self.insp = None
        self.meta_original = MetaData()
        self.relations = {}
        self.original_relations_names = []

        #self.meta_new = MetaData()
        # A dictionary with lists, each with the names of its decomposed relations
        self.decomposition_match = {}



    def compute_normalization_proposal(self, decomp='3NF'):
        self.delete_BCNF_decomposition_proposal()
        decomposition_dic = {}
        for name in self.original_relations_names:
            dec = Decomposition()
            rel = self.relations[name]
            attr = rel.attributes
            canonical_cover = rel.canonical_cover
            # Decomposition proposal:
            dec_relation_list = []

            # Caso en que no hay FDs
            if len(rel.fds) == 0:
                sub_name = name + "_1"
                new_relation = rel.sub_relation(sub_name, attr)
                self.relations[sub_name] = new_relation
                new_relation.set_candidate_keys()
                new_relation.set_normalization()
                decomposition_dic[name] = [sub_name]
            elif rel.NF == 'BCNF':
                sub_name = name + "_1"
                new_relation = rel.sub_relation(sub_name, attr, rel.fds)
                self.relations[sub_name] = new_relation
                new_relation.set_canonical_cover()
                new_relation.set_candidate_keys()
                new_relation.set_normalization()

                new_relation.join_rhs_fds()
                new_relation.join_rhs_cc()

                decomposition_dic[name] = [sub_name]
            else:
                if decomp == '3NF':
                    print(canonical_cover)
                    dec_proposal = dec.proposal3NF(set(attr), canonical_cover, (rel.fds))
                else:
                    dec_proposal = dec.proposalBCNF(set(attr), canonical_cover)

                # Saves the decomposition in a dictionary:

                i = 1

                for tup in dec_proposal:
                    sub_name = name + '_' + str(i)
                    dec_relation_list.append(sub_name)
                    new_attr = list(tup[0])
                    new_fds = FDependencyList(tup[1])
                    new_relation = rel.sub_relation(sub_name, new_attr, new_fds)

                    new_relation.set_canonical_cover()
                    new_relation.set_candidate_keys()
                    new_relation.set_normalization()

                    new_relation.join_rhs_fds()
                    new_relation.join_rhs_cc()

                    self.relations[sub_name] = new_relation
                    i += 1

                decomposition_dic[name] = dec_relation_list

        self.decomposition_match = decomposition_dic



    def delete_BCNF_decomposition_proposal(self):
        print(self.decomposition_match)
        print(self.decomposition_match.keys())
        for rel_name in self.decomposition_match.keys():
            dec_list = self.get_decomposition_names(rel_name)
            for dec in dec_list:
                del self.relations[dec]

    def compute_sql_statements(self):
        meta_new = MetaData()
        filename = "Queries.sql"
        f = open(filename, 'w')
        f.write('\n')
        f.close()
        keys =list(self.decomposition_match.keys())
        f = open(filename,'a')
        for relation in keys:
            m = self.get_decomposition_names(relation)
            for subrelation in m:
                s = self.relations[subrelation].SQL_statement(meta_new)
                l = CreateTable(s)
                print(l)
                f.write(str(l))
        f.close()



    def set_db_connection_params(self, username, password, host, database, port):
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.port = port

    def get_metadata(self):
        conn_string = 'postgresql://' + str(self.username) + ':' + str(self.password) + '@' + str(self.host) + '/' + \
                      str(self.database)
        print(conn_string)
        self.engine = create_engine(conn_string)
        self.meta_original.reflect(bind=self.engine)
        self.insp = inspect(self.engine)

    def get_schema(self):
        db_schema = {}
        tables = self.insp.get_table_names()
        for name in tables:
            att = self.insp.get_columns(name)
            pk = self.insp.get_pk_constraint(name)
            unique = self.insp.get_unique_constraints(name)
            rel = Relation(name, schema_attributes=att, schema_keys=pk, schema_unique=unique)
            db_schema[name] = rel

        self.original_relations_names = tables
        self.relations = db_schema

    def append_fds(self):
        names = list(self.relations.keys())
        for i in range(0,len(names)):
            nam = names[i]
            print("-------------Reading:------------", nam)
            partitions_dict = get_table_partitions(nam, self.relations[nam].attributes, self.engine)
            print("---------------------------------")
            print(self.relations[nam])
            self.relations[nam].find_fds(partitions_dict)

            # Compute the canicalcover, candidate keys and normal form
            self.relations[nam].set_canonical_cover()
            self.relations[nam].set_candidate_keys()
            self.relations[nam].set_normalization()

            self.relations[nam].join_rhs_fds()
            self.relations[nam].join_rhs_cc()
            #print(self.relations[nam])

    def update_relation(self, relation_name):
        self.relations[relation_name].set_canonical_cover()
        self.relations[relation_name].set_candidate_keys()
        self.relations[relation_name].set_normalization()

        self.relations[relation_name].join_rhs_fds()
        self.relations[relation_name].join_rhs_cc()

    def get_NF(self, relation_name):
        return self.relations[relation_name].NF

    def get_candidate_keys(self, relation_name):
        return self.relations[relation_name].candidate_keys

    def get_canonical_cover(self, relation_name):
        return self.relations[relation_name].canonical_cover

    def get_fds(self,relation_name):
        return self.relations[relation_name].fds

    def get_decomposition_names(self, relation_name):
        return self.decomposition_match[relation_name]

    def get_decomposition_names_all(self):
        l = []
        for i in self.decomposition_match:
            l.append(i)
        return l

    def get_original_relations_names(self):
        return self.original_relations_names

    def get_relation_names(self):
        return self.relations.keys()

    def get_relation(self, relation_name):
        return self.relations[relation_name]

    def get_relation_attributes(self, relation_name):
        return self.relations[relation_name].attributes

    def remove_fd_idx(self, relation_name, idx):
        rel = self.get_relation(relation_name)
        removed = rel.fds.remove_fd_idx(idx)
        return removed

    def add_fd(self, fd_dic, relation_name):
        rel = self.get_relation(relation_name)
        lhs = fd_dic['lhs'].split(",")
        lhs_format = [x.strip() for x in lhs]
        rhs = fd_dic['rhs'].split(",")
        rhs_format = [x.strip() for x in rhs]
        fd = FDependency(lhs_format, rhs_format)
        rel.fds_add(fd)

    def get_attr_closure(self, attr_dic, relation_name):
        rel = self.get_relation(relation_name)
        attributes = attr_dic['attr'].split(",")
        attributes_format = [x.strip() for x in attributes]
        closure = rel.fds.attribute_closure(attributes_format)
        return closure

    def get_violation(self, relation_name, nf='2NF'):
        rel = self.get_relation(relation_name)
        if nf == '2NF':
            ret = rel.normalization.FDList2NF
        elif nf == '3NF':
            ret = rel.normalization.FDList3NF
        else:
            ret = rel.normalization.FDListBCNF
        return ret

    def get_relation_db_schema_attributes(self, relation_name):
        rel = self.get_relation(relation_name)
        return rel.db_schema_attributes

    def get_relation_db_schema_unique(self, relation_name):
        rel = self.get_relation(relation_name)
        return rel.db_schema_unique

    def get_relation_db_schema_pk(self, relation_name):
            rel = self.get_relation(relation_name)
            return rel.db_schema_pk

    def add_user_relation(self, relation_name):
        if relation_name not in self.original_relations_names:
            self.original_relations_names.append(relation_name)
            self.relations[relation_name] = Relation(relation_name)
            return 0
        else:
            return 1


    def add_user_relation_attribute(self, relation_name, attribute_name):
        rel = self.get_relation(relation_name)
        return rel.add_attributes(attribute_name)

