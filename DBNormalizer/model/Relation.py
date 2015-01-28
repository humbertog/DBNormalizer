
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

    def SQL_statement(self, metadata):
        """
        Returns an object of class Table (see parse_table function) that can be used to send the CREATE TABLE statement
        to the database. This method needs, at least, the schema_attributes attribute.
        :param metadata: metadata (SQLAlchemy)
        :return: and object of class table
        """
        name = self.name
        column_schema = self.db_schema_attributes  # Mandatory
        pk_schema = self.db_schema_pk
        unique_schema = self.db_schema_unique
        return parse_table(name, metadata, column_schema_list=column_schema, pk_schema=pk_schema,
                           unique_schema=unique_schema)

    def sub_relation(self, name, over_attributes):
        """
        Returns a sub-relation over the attributes specified. The pk and unique constraints are dropped if
        they are not defined completely in the sub-relation. If the schema_attributes, schema_pk and schema_unique
        are defined, the method will use them to obtain the new sub-relation.
        :param name: name of the new relation
        :param over_attributes: the attributes that the sub-relation must contain
        :return:
        """
        new_schema_attr = decompose_schema_attributes(self.db_schema_attributes, over_attributes)
        new_schema_pk = decompose_schema_pk(self.db_schema_pk, over_attributes)
        new_schema_unique = decompose_schema_unique(self.db_schema_unique, over_attributes)

        new_relation = Relation(name, schema_attributes=new_schema_attr, schema_keys=new_schema_pk,
                                schema_unique=new_schema_unique)

        # Here is missing the code to determine which FDs still hold in the sub relation
        # Once we have the Fds left in the sub-relation we can compute the candidate keys and normal forms.

        return new_relation