__author__ = 'Nantes'
from DBNormalizer.model.FDependencyList import *
from DBNormalizer.model.findFDs import find_fds
from DBNormalizer.model.SQLParser import *
from DBNormalizer.model.Normalization import *


class Relation:

    def __init__(self, name, attributes=None, schema_attributes=None, schema_keys=None, schema_unique=None):
        self.name = name
        self.attributes = attributes
        self.key = []
        self.unique = []
        self.fds = FDependencyList()
        self.NF = None

        # Normalization
        self.normalization = Normalization()
        self.NF = None
        self.candidate_keys = []
        self.canonical_cover = FDependencyList()

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
        return str("Name: ") + str(self.name) + "\n" + "Attributes: " + str(self.attributes) + \
               "\n" + "PK: " + str(self.key) + "\n" + "Unique: " + str(self.unique) + "\n"\
               + "FDS: " + str(self.fds) + "\n" + "CC:" + str(self.canonical_cover) + "\n" + "Cand keys:" + \
               str(self.candidate_keys) + "\n" + "NF: " + str(self.NF)

    def join_rhs_cc(self):
        new_fds = FDependencyList()
        old_fds = self.canonical_cover[:]
        while len(old_fds) > 0:
            fds_sel = old_fds.pop()
            i = 0
            while i < len(old_fds):
                fd = old_fds[i]
                if fds_sel.lh == fd.lh:
                    fds_sel.rh = fds_sel.rh + fd.rh
                    old_fds.pop(i)
                i+=1
            new_fds.append(fds_sel)

        self.canonical_cover = new_fds

    def join_rhs_fds(self):
        new_fds = FDependencyList()
        old_fds = self.fds[:]
        while len(old_fds) > 0:
            fds_sel = old_fds.pop()
            i = 0
            while i < len(old_fds):
                fd = old_fds[i]
                if fds_sel.lh == fd.lh:
                    fds_sel.rh = fds_sel.rh + fd.rh
                    old_fds.pop(i)
                i+=1
            new_fds.append(fds_sel)
        self.fds = new_fds


    def get_attributes_type(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='type', attr_name=attr_name)

    def get_attributes_autoincrement(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='autoincrement',
                                             attr_name=attr_name)

    def get_attributes_nullable(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='nullable', attr_name=attr_name)

    def get_attributes_default(self, attr_name=None):
        return get_schema_attribute_property(self.db_schema_attributes, att_property='default', attr_name=attr_name)

    def add_attributes(self, attributes):
        if self.attributes is None:
            self.attributes = [attributes]
            return 0
        elif attributes not in self.attributes:
            self.attributes.append(attributes)
            return 0
        else:
            return 1

    def set_canonical_cover(self):
        if len(self.fds) > 0:
            self.canonical_cover = self.fds.MinimalCover()
            self.join_rhs_cc()

    def set_candidate_keys(self):
        if len(self.canonical_cover) != 0:
            self.candidate_keys = self.normalization.findCandKeys(set(self.attributes), self.canonical_cover, self.fds)
        else:
            self.candidate_keys = [set(self.attributes)]

    def set_normalization(self):
        if len(self.canonical_cover) != 0:
            self.normalization.FDListBCNF = FDependencyList()
            self.normalization.FDList3NF = FDependencyList()
            self.normalization.FDList2NF = FDependencyList()
            for fd in self.canonical_cover:
                lhs=set(fd.lh)
                rhs=set(fd.rh)
                self.normalization.check2NF(fd,lhs,rhs, self.candidate_keys)
                self.normalization.check3NF(fd, lhs, rhs, self.candidate_keys)
                self.normalization.checkBCNF(fd, lhs, rhs, self.candidate_keys)

            if len(self.normalization.FDList2NF) != 0:
                self.NF = '1NF'
            elif len(self.normalization.FDList3NF) != 0:
                self.NF = '2NF'
            elif len(self.normalization.FDListBCNF) != 0:
                self.NF = '3NF'
            else:
                self.NF = 'BCNF'

        else:
            self.normalization.FDListBCNF = FDependencyList()
            self.normalization.FDList3NF = FDependencyList()
            self.normalization.FDList2NF = FDependencyList()
            self.NF = 'NoFDs'

    def fds_add(self, fd):
        if type(fd) is FDependencyList:
            self.fds.extend(fd)
        if type(fd) is FDependency:
            self.fds.append(fd)

    def fds_remove(self, fd):
        if type(fd) is FDependency:
            self.fds.remove(fd)

    def find_fds(self, db_partition, test_mode=False, pk=[], uk=[]):
        """
        Calls find_fds from SQLParser and computes minimal cover
        :param db_partition:
        """
        fds = FDependencyList()
        fds_in_rel = find_fds(self.attributes, db_partition, test_mode, pk=self.key, uk=self.unique)
        for rhs in fds_in_rel.keys():
            if fds_in_rel[rhs]:
                for lhs in fds_in_rel[rhs]:
                    fds.append(FDependency(lhs, [rhs]))
        self.fds = fds.MinimalCover()
        self.join_rhs_fds()
        #self.fds = fds

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

    def sub_relation(self, name, over_attributes, fds=None):
        """
        Returns a sub-relation over the attributes specified. The pk and unique constraints are dropped if
        they are not defined completely in the sub-relation. If the schema_attributes, schema_pk and schema_unique
        are defined, the method will use them to obtain the new sub-relation.
        :param name: name of the new relation
        :param over_attributes: the attributes that the sub-relation must contain
        :return:
        """
        if self.db_schema_attributes:
            new_schema_attr = decompose_schema_attributes(self.db_schema_attributes, over_attributes)
            new_schema_pk = decompose_schema_pk(self.db_schema_pk, over_attributes)
            new_schema_unique = decompose_schema_unique(self.db_schema_unique, over_attributes)

            new_relation = Relation(name, schema_attributes=new_schema_attr, schema_keys=new_schema_pk,
                                    schema_unique=new_schema_unique)
        else:
            new_relation = Relation(name, over_attributes)
        if fds is not None:
            new_relation.fds_add(fds)
            new_relation.join_rhs_fds()

        return new_relation

