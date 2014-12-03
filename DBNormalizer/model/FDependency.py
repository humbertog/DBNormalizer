__author__ = 'humberto'

from ..model.FDependencyList import *


class FDependency:
    """
    Functional dependency class
    """
    def __init__(self, lh, rh):
        self.lh = lh
        self.rh = rh

    def __str__(self):
        """
        Printing method for the class
        :return: string which is printed
        """
        return str(self.lh) + ' -> ' + str(self.rh)

    def __eq__(self, other):
        """
        Returns true if self is equal to other
        :param other: an FDependency object
        :return: true or false
        """
        # Use set to compare, otherwise repeated elements are allowed
        return set(self.lh) == set(other.lh) and set(self.rh) == set(other.rh)

    def as_singleton(self):
        """
        Returns the singletons in a functional dependency, i.e., the functional dependencies with only one attribute in
        the right hand side. If fd=[A,B]->[C,D], then [A,B]->[C] and [A,B]->[D]
        :return: a FDependency object with singletons
        """
        fd_list = []
        for rh in self.rh:
            fd_list.append(FDependency(self.lh, [rh]))
        return FDependencyList(fd_list)
