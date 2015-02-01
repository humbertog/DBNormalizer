__author__ = 'Humberto'

from DBNormalizer.model.FDependencyList import *


# Instantiate 3 FDs objects:
fd1 = FDependency(['A'], ['C', 'D']) # means A -> CD
fd2 = FDependency(['B'], ['C'])
fd3 = FDependency(['C', 'D'], ['E'])

# Instantiate an object that contains a list of FDs:
fds = FDependencyList([fd2, fd3])
fds.append(fd1)  # This class inherits from list so you can use any list method!
#print(fds)
print("fucking FDs",fds)
# Computes the attribute closure of AB with the FDs contained
# in fds
closure = fds.attribute_closure(['A', 'B'])
print(closure)

# Returns singleton fds:
# If AB -> ACD, then AB->A, AB->C and AB->D RETURNS A FDependencyList

singleton_from_fd_list = fds.makeRightsingleton()
print(singleton_from_fd_list)
