__author__ = 'humberto'

from DBNormalizer.model.Relation import *

# Give fds of a hypothetical database (for testing purposes):
fd1 = FDependency(['A'], ['E']) # means A -> CD
fd2 = FDependency(['B'], ['C'])
fd3 = FDependency(['C','D'], ['E'])

fds1 = FDependencyList([fd1,fd2, fd3])
print(fds1)
# Finds the fds that satisfies the given lhs and rhs. The idea of this function is to eliminate unnecessary computation
# using th fact that, if the fd X->E does not hold, then for all Y subset of X, Y->E doesn't hold either.

# Creates a relation with only name and attributes
relation1 = Relation('Test', ['A', 'B', 'C', 'D', 'E'])
# Find the fds in the database (for testing purposes suppose the database is one in which fds1 hold)
print(relation1)
relation1.find_fds(fds1)
print(relation1.fds)

