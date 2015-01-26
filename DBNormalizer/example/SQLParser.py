__author__ = 'humberto'

from DBNormalizer.model.FDependencyList import *
from DBNormalizer.model.SQLParser import *

# Give fds of a hypothetical database (for testing purposes):
fd1 = FDependency(['A'], ['E']) # means A -> CD
fd2 = FDependency(['B'], ['C'])
fd3 = FDependency(['C','D'], ['E'])

fds1 = FDependencyList([fd1,fd2, fd3])
print(fds1)

# Finds the fds that satisfies the given lhs and rhs. The idea of this function is to eliminate unnecessary computation
# using th fact that, if the fd X->E does not hold, then for all Y subset of X, Y->E doesn't hold either.
res = find_fds_rhs(['A', 'B', 'C', 'D'], ['E'], fds1)
print(res)


