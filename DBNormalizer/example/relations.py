__author__= 'Gabriela'
from DBNormalizer.model.Relation import *

# Instantiate 3 FDs objects:
fd1 = FDependency(['A'], ['C', 'D']) # means A -> CD
fd2 = FDependency(['B'], ['C'])
fd3 = FDependency(['C', 'D'], ['E'])

# Instantiate an object that contains a list of FDs:
fds = FDependencyList([fd2, fd3])

# Instantiate a relation containing name, attributes, domain, keys, and FDs
relation1 = Relation("User", ["uid", "username", 'password', 'date', 'geotag', 'gravatar'],
                     ["integer", 'character','character',  'date,point','bytea'], "uid", fds)

print(relation1)