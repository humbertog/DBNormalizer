
from DBNormalizer.model.FDependencyList import *
from DBNormalizer.model.findFDs import find_fds

class Relation:
    relCount = 0

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.keys = []
        self.fds = FDependencyList()
        Relation.relCount += 1

    def __str__(self):
        return str("Name:") + str(self.name) + "\n" + "Attributes:" + str(self.attributes) + \
               "\n" + str("Keys: ") + str(self.keys) + "\n" + str("FDS: ") + str(self.fds)

    def get_attributes(self):
        attributes = []
        for x in self.attributes:
            attributes.append(x['name'])
        return attributes

    def get_attributes_property(self, property='type', attr_name=None):
        attributes = []
        if attr_name is None:
            for x in self.attributes:
                attributes.append(x[property])
        else:
            attributes = [x[property] for x in self.attributes if x['name'] == attr_name]
        return attributes

    def get_attributes_type(self, attr_name=None):
        return self.get_attributes_property(property='type', attr_name=attr_name)

    def get_attributes_autoincrement(self, attr_name=None):
        return self.get_attributes_property(property='autoincrement', attr_name=attr_name)

    def get_attributes_nullable(self, attr_name=None):
        return self.get_attributes_property(property='nullable', attr_name=attr_name)

    def get_attributes_default(self, attr_name=None):
        return self.get_attributes_property(property='default', attr_name=attr_name)

    def find_fds(self, db_partition):
        """
        Calls find_fds from SQLParser and computes minimal cover
        :param db_partition:
        """
        fds = FDependencyList()
        fds_in_rel = find_fds(self.attributes, db_partition)
        for rhs in fds_in_rel.keys():
            if fds_in_rel[rhs]:
                for lhs in fds_in_rel[rhs]:
                    fds.append(FDependency(lhs, [rhs]))
        self.fds = fds.MinimalCover()