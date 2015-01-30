__author__ = 'humberto'

from DBNormalizer.model.Relation import Relation
from DBNormalizer.model.SQLParser import get_table_partitions
from sqlalchemy import *


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
        self.relations_original = None
        self.meta_new = None
        self.new_relations = None

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

        self.relations = db_schema

    def append_fds(self):
        names = list(self.relations.keys())
        for i in range(0,len(names)):
            nam = names[i]
            partitions_dict = get_table_partitions(nam, self.relations[nam].attributes, self.engine)
            self.relations[nam].find_fds(partitions_dict)
            #print(self.relations[nam])
