__author__ = 'humberto'


class FDependency:
    def __init__(self, lh, rh):
        self.lh = lh
        self.rh = rh

    def __str__(self):
        return str(self.lh) + ' -> ' + str(self.rh)

    def __eq__(self, other):
        return set(self.lh) == set(other.lh) and set(self.rh) == set(other.rh)

    def as_singleton(self):
        fd_list = []
        for rh in self.rh:
            fd_list.append(FDependency(self.lh, [rh]))
        return FDependencyList(fd_list)


class FDependencyList(list):
    def __str__(self):
        string = ''
        for i in range(self.__len__()):
            if i == 0:
                string = string + self[i].__str__()
            else:
                string = string + ', ' + self[i].__str__()
        return string

    def attribute_closure(self, attributes):
        unused = self[:]
        closure = set(attributes)
        closure_len = 0
        while closure.__len__() != closure_len:
            closure_len = closure.__len__()
            for fd in unused:
                if set(fd.lh).issubset(closure):
                    closure = closure.union(set(fd.rh))
                    unused.remove(fd)
        return list(closure)

    def as_singleton(self):
        singleton_list = []
        for fd in self:
            singleton_list = singleton_list + fd.as_singleton()
        return FDependencyList(singleton_list)
