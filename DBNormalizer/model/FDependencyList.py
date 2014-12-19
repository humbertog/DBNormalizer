__author__ = 'humberto'

from DBNormalizer.model.FDependency import *

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


    def MinimalCover(self):
        Frs = makeRightsingleton(self)
        Fex =removeExtraneous(Frs)
        Fmin = removeDuplicate(Fex)
        return [Fmin]

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

    def removeExtraneous(self):
        ExtraneousList=[]
        exFlag=0
        for fd in self:
            lhs = fd.lh
            rhs = fd.rh
            if len(lhs)>1:
                for attr in lhs:
                    if self.computeClosureNcheck(attr,rhs):
                        ExtraneousList.append(FDependency([attr],rhs))
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
