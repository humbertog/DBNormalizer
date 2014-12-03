__author__ = 'humberto'


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


class FDependencyList(list):
    """
    Functional dependency class
    """
    def __str__(self):
        """
        Printing method for the class
        :return: string which is printed
        """
        string = ''
        for i in range(self.__len__()):
            if i == 0:
                string = string + self[i].__str__()
            else:
                string = string + ', ' + self[i].__str__()
        return string

    def attribute_closure(self, attributes):
        """
        Computes the attribute closure with respect to the functional dependencies in the list
        :param attributes: list of attributes for which the closure is to be computed
        :return: list containing the attributes closure
        """
        unused = self[:]    # Copies the self (list)
        closure = set(attributes)       # Stores the attribute closure. Is set because no repeated attributes allowed.
        closure_len = 0                 # Used as stopping condition
        while closure.__len__() != closure_len:
            closure_len = closure.__len__()
            for fd in unused:
                if set(fd.lh).issubset(closure):
                    closure = closure.union(set(fd.rh))
                    unused.remove(fd)
        return list(closure)    # Casts the set object to a list

    def as_singleton(self):
        """
        Returns all singletons that could be deduced from the functional dependencies
        :return: list with all functional dependencies' singletons
        """
        singleton_list = []
        for fd in self:
            singleton_list = singleton_list + fd.as_singleton()
        return FDependencyList(singleton_list)

