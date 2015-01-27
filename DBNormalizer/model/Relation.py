
from DBNormalizer.model.FDependencyList import *
from DBNormalizer.model.findFDs import find_fds
from DBNormalizer.model.SQLParser import *


class Relation:

    def __init__(self, name, attributes=None, schema_attributes=None, schema_keys=None, schema_unique=None):
        self.name = name
        self.attributes = attributes
        self.key = None
        self.unique = None
        self.fds = FDependencyList()
        self.NF = None

        self.db_fds = None

        self.db_schema_attributes = schema_attributes
        self.db_schema_pk = schema_keys
        self.db_schema_unique = schema_unique


        if schema_attributes:
            self.attributes = get_schema_attribute_property(self.db_schema_attributes, att_property='name')
        if schema_keys:
            self.key = get_schema_keys(self.db_schema_pk)
        if schema_unique:
            self.unique = get_schema_unique(self.db_schema_unique)

    def __str__(self):
        return str("Name:") + str(self.name) + "\n" + "Attributes:" + str(self.attributes) + \
               "\n" + str("PK: ") + str(self.key) + "\n" + str("Unique:") + str(self.unique) + "\n"\
               + str("FDS: ") + str(self.fds)

    def get_attributes_type(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='type', attr_name=attr_name)

    def get_attributes_autoincrement(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='autoincrement',
                                             attr_name=attr_name)

    def get_attributes_nullable(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='nullable', attr_name=attr_name)

    def get_attributes_default(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='default', attr_name=attr_name)

    def fds_add(self, fd):
        if type(fd) is FDependencyList:
            self.fds.extend(fd)
        if type(fd) is FDependency:
            self.fds.append(fd)

    def fds_remove(self, fd):
        if type(fd) is FDependency:
            self.fds.remove(fd)

    def find_fds(self, db_partition, test_mode=False):
        """
        Calls find_fds from SQLParser and computes minimal cover
        :param db_partition:
        """
        fds = FDependencyList()
        fds_in_rel = find_fds(self.attributes, db_partition, test_mode)
        for rhs in fds_in_rel.keys():
            if fds_in_rel[rhs]:
                for lhs in fds_in_rel[rhs]:
                    fds.append(FDependency(lhs, [rhs]))
        self.fds = fds.MinimalCover()