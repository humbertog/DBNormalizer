__author__ = 'mariaslanova'
# TODO Remove file as now this functions are part of FunctionalDependencyList
from DBNormalizer.model.FDependencyList import *

# This file should be removed
def MinimalCover(F):
    Frs = makeRightsingleton(F)
    Fex =removeExtraneous(Frs)
    Fmin = removeDuplicate(Fex)
    return [Fmin]


def makeRightsingleton(F):
    singletonList=[]
    for fd in F:
        lhs = fd.lh
        rhs = fd.rh
        if len(rhs)>1:
            for attr in rhs:
             singletonList.append(FDependency(lhs, [attr]))
        else:
            singletonList.append(FDependency(fd.lh,fd.rh))
    return FDependencyList(singletonList)


def contains(closureList,rhs):
    if closureList.count(rhs[0])>=1:
        return 1
    else:
        return 0


def computeClosureNcheck(F,attr,rhs):
    if (contains(F.attribute_closure(attr),rhs))==1:
        return 1
    else:
        return 0


def removeExtraneous(F):
    ExtraneousList=[]
    exFlag=0
    for fd in F:
        lhs = fd.lh
        rhs = fd.rh
        if len(lhs)>1:
            for attr in lhs:
                if computeClosureNcheck(F,attr,rhs):
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


def removeDuplicacy(F):
    i=0
    while i < len(F):
        fd = F[i]
        lhs = fd.lh
        rhs = fd.rh
        temp=F.copy()
        temp.remove(fd)
        if computeClosureNcheck(FDependencyList( temp),lhs,rhs)==1:
            F.remove(fd)
            continue
        else:
            i=i+1
    return F
