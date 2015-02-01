__author__ = 'mariaslanova','Bishnu','Harsha'

from itertools import combinations
from DBNormalizer.model.mincover import *
from DBNormalizer.model.FDependencyList import *

class Normalization:
#lhs is a set of LHS attributes
#candKeys is a set of all candidate Keys {{a,b},{bcd}}
#key is boolean to store if lhs is key or not

    def __init__(self):
        self.FDList2NF=FDependencyList()
        self.FDList3NF=FDependencyList()
        self.FDListBCNF=FDependencyList()
        self.FDListNoNF=FDependencyList()

    def isKey(self,lhs, candKeys):
        key = False
        if (candKeys.__contains__(lhs)):
            key = True
        return key

    #rhs is set
    #singleton is boolean variable
    def isSingleton(self,rhs):
        singleTon = False
        l =rhs.__len__()
        if (l == 1):
            singleTon = True
        return singleTon


    #attr is a single Attribute
    #candKeys is set of candidate keys
    #prime is boolean variable
    def isNonPrime(self,attr, candKeys):
        prime = False
        for key in candKeys:
            if (key.__contains__(attr)):
                Prime = True
                break
        return not prime


    #lhs is set of LHS attributes
    #key is a single key in set format extracted from allKeys
    #propersubset is boolean variable
    def isProperSubset(self,lhs, key):
        propersubset = False
        if (lhs.issubset(key) and not key.issubset(lhs)):
            propersubset = True
        return propersubset


    #S is set
    #subs is a list of all the non empty subsets of S subs=[{a},{b},{a,b}]
    def findNonEmptySubsets(self,S):
        subs = [set(j) for i in range(len(S)) for j in list(combinations(S, i + 1))]
        return subs


    #minFDs is the list of Minimum Cover of R over FDs
    #LRset=[{LHSs},{RHSs}]
    #L={LHSs}
    #R={RHSs}
    def getLnRSet(self,minFDs):
        LRset = list()
        L = []
        R = []
        for fd in minFDs:
            L.extend(fd.lh)
            R.extend(fd.rh)
        LRset.append(set(L))
        LRset.append(set(R))
        return LRset


    #R={all the attributes}
    #S=[{LHSs},{RHSs}]
    #necessary is the necessary attributes
    def getNecessaryAttribute(self,R, minFDs):
        S = Normalization.getLnRSet(self,minFDs)
        necessary = R.difference(S[0].union(S[1]))
        necessary = necessary.union(S[0].difference(S[1]))
        return necessary


    #R={all the attributes}
    #S=[{LHSs},{RHSs}]
    #useless is the useless attributes
    def getUseLessAttribute(self,R, minFDs):
        S = Normalization.getLnRSet(self,minFDs)
        useless = S[1].difference(S[0])
        return useless


    #X is the set of Necessary Attributes
    #Y is the set Useless Attributes
    #M is the set of neither Necessary nor Useless
    def getUsefulAttribute(self,R, X, Y):
        #X=getNecessaryAttribute(R,minFDs)
        #Y=getUseLessAttribute(R,minFDs)
        M = R.difference(X.union(Y))
        return M


    #X is set to be added to each elements(sets) of L
    #L is set of sets
    def addedL(self,L, X):
        L1 = list()
        for Z in L:
            L1.append(Z.union(X))
        return L1


    #candKeys is the List of Sets of candidate Key
    #zclosure is set that contains closure of Z
    def findCandKeys(self,R, minFDs,FDs):
        candKeys = list()
        X = self.getNecessaryAttribute(R, minFDs)
        #print(X)
        Y = self.getUseLessAttribute(R, minFDs)
        #print(Y)
        M = self.getUsefulAttribute(R,X, Y)
        #print(M)
        L = self.findNonEmptySubsets(M)
        if(X!=set()):
            xclosure =set(FDs.attribute_closure(X))
            #print(xclosure)
            if (xclosure == R):
                #print("True")
                candKeys.append(X)
                #print(candKeys)
            else:
                L = self.addedL(L, X)


        #L = self.findNonEmptySubsets(M)
        #L = self.addedL(L, X)
        #print(L)
        #i = 0
        while L != []:
            #i = i + 1
            Z = L[0]
            del L[0]
            zclosure = set(FDs.attribute_closure(Z))
            if (zclosure == R):
                #candKeys=self.addNewKey(Z,candKeys)
                candKeys.append(Z)
                #candKeys=self.removeSuperSet(Z,candKeys)
                L=self.removeSuperSet(Z, L)
        return candKeys


    def removeSuperSet(self,Z, L):
        L1 = L.copy()
        for l in L1:
            if (Z.issubset(l)):
                L.remove(l)
        return L


    def findClosure(Fds,attr):
        closure=Fds.attribute_closure(attr)
        return set(closure)


    #keys=[set(l) for l in allKeys]
    #print(keys)
    #violation2nf variable keeps the state of violation [true or false]
    #isSigleton(fd) checks if given fd is singleton (rightside with single attribute)
    #candKeys is list of candidate Keys computed beforehand
    #isProperSubset(lhs, key) checks if lhs is a proper subset of key.
    #nonPrime(rhs) checks if rhs is a non Prime attribute
    def check2NF(self,fd, lhs, rhs, candKeys):
        violation2NF = False
        if (self.isSingleton(rhs)):
            for key in candKeys:
                if (self.isProperSubset(lhs, key)):
                    if (self.isNonPrime(rhs,candKeys)):
                        violation2NF = True
                        self.FDList2NF.append(fd)
                        break
        return violation2NF


    #iskey(lhs,candKeys) test if lhs is key
    #toAttributeList(rhs) get the all the attributes in right Hand side as a List
    def check3NF(self,fd, lhs, rhs, candKeys):
        violation3NF = False
        if (self.isKey(lhs, candKeys)):
            violation3NF = False
        else:
            for attr in rhs:
                if (self.isNonPrime(attr, candKeys)):
                    violation3NF = True
                    self.FDList3NF.append(fd)
                    break
        return violation3NF


    #lhs and rhs are set of LHS and RHS attributes respectively
    def checkBCNF(self,fd, lhs, rhs, candKeys):
        violationBCNF = False
        if (not self.isKey(lhs, candKeys)):
            violationBCNF = True
            self.FDListBCNF.append(fd)
        return violationBCNF

