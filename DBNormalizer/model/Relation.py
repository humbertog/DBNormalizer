
from DBNormalizer.model.FDependencyList import *

class Relation:
    relCount = 0

    def __init__(self, name, attributes, domain, keys, fds):
        self.name = name
        self.attributes = attributes
        self.domain = domain
        self.keys = keys
        self.fds = fds
        Relation.relCount += 1

    def __str__(self):
        return str("Name:") + str(self.name) + "\n" + "Attributes:" + str(self.attributes) + "\n" + str("Domain:") \
               +  str(self.domain) + "\n" + str("Keys: ") + str(self.keys) + "\n" + str("FDS: ") + str(self.fds)



