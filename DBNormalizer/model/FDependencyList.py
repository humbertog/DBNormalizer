__author__ = 'humberto'

from DBNormalizer.model.FDependency import *
from itertools import combinations

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
        unused = self[:]   # Copies the self (list)
        closure = set(attributes)       # Stores the attribute closure. Is set because no repeated attributes allowed.
        closure_len = 0                 # Used as stopping condition

        while closure.__len__() != closure_len:
            closure_len = closure.__len__()
            unused_t = unused[:]
            for fd in unused:
                if set(fd.lh).issubset(closure):
                    unused_t.remove(fd)
                    closure = closure.union(set(fd.rh))
            unused = unused_t[:]
        return list(closure)    # Casts the set object to a list


    def MinimalCover(self):
        return self.makeRightsingleton().removeExtraneous().removeDuplicacy()

    def get_lhs(self):
        attr = set()
        for fd in self:
            attr = attr.union(set(fd.lh))
        return list(attr)

    def get_rhs(self):
        attr = set()
        for fd in self:
            attr = attr.union(set(fd.rh))
        return list(attr)

    def candidate_keys(self):
        keys = list()
        lhs = set(self.get_lhs())
        rhs = set(self.get_rhs())
        attributes_in_fds = lhs.union(rhs)
        for att in lhs:
            closure = self.attribute_closure(list(att))
            if set(closure) == attributes_in_fds:#in general it should be R

                keys.append(list(att))

        i = 2
        #while keys.__len__() == 0 and i <= lhs.__len__():
        while i <= lhs.__len__():
            left = set(combinations(lhs, i))
            for k in left:
                closure = self.attribute_closure(list(k))
                if set(closure) == attributes_in_fds:
                    keys.append(list(k))
            i += 1
        return keys


    def makeRightsingleton(self):
        singletonList=[]
        for fd in self:
            lhs = fd.lh
            rhs = fd.rh
            if len(rhs)>1:
                for attr in rhs:
                    singletonList.append(FDependency(lhs, [attr]))
            else:
                singletonList.append(FDependency(fd.lh,fd.rh))
        return FDependencyList(singletonList)


    def computeClosureNcheck(self, attr, rhs):
        def contains(closureList, rhs):
            if closureList.count(rhs[0]) >= 1:
                return 1
            else:
                return 0

        if (contains(self.attribute_closure(attr),rhs))==1:
            return 1
        else:
            return 0
    def findNonEmptySubsets(self,S):
        subs = [set(j) for i in range(len(S)) for j in list(combinations(S, i + 1))]
        return subs

    def removeExtraneous(self):
        ExtraneousList=[]
        exFlag=0
        for fd in self:
            lhs = fd.lh
            rhs = fd.rh
            if len(lhs)>1:
                L=[list(j) for i in range(len(lhs)) for j in list(combinations(set(lhs),i+1))]
                for attr in L:
                    if self.computeClosureNcheck(attr,rhs):
                        ExtraneousList.append(FDependency(attr,rhs))
                        exFlag=1
                        break
                    else:
                        exFlag=0
                if exFlag==0:
                    ExtraneousList.append(FDependency(lhs,rhs))
            else:
                ExtraneousList.append(FDependency(lhs,rhs))
        return FDependencyList(ExtraneousList)

    def removeDuplicacy(self):
        i=0
        while i < len(self):
            fd = self[i]
            lhs = fd.lh
            rhs = fd.rh
            temp=self.copy()
            temp.remove(fd)
            if FDependencyList(temp).computeClosureNcheck(lhs,rhs) == 1:
                self.remove(fd)
                continue
            else:
                i = i+1
        return self
