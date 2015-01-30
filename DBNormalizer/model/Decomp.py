__author__ = 'mariaslanova','Bishnu','Harsha'

from DBNormalizer.model.Normalization import *
class Decomposition:
    def __init__(self):
        self.List_Relation=list()
    #def combineSingleTonFD(self,MinFDs):

    def proposal3NF(self,R,MinFDs,Fds):
        #FDs=self.combineSingleTonFD(MinFDs)
        FDs=Fds
        for fd in MinFDs:
            R1=self.createNewRelation(fd)
            #self.List_Relation.append(R1)
            self.addRelation(R1)

        if not self.candidateKeyChecking(R,MinFDs,FDs):
            KRs=self.createKeyRelation(R,MinFDs,FDs)

            self.List_Relation.append(KRs[0])


        return self.List_Relation
    #testing Phase
    def proposalBCNF(self,R0,F0):
        accum=list()
        L=self.decomposeBCNF(R0,F0,accum)
        print("----start Recursive Call------")
        return L
    def decomposeBCNF(self,R0,F0,accum):
        print("-----Start of a call")
        print("call with:",R0,F0)
        norm=Normalization()
        candKeys=norm.findCandKeys(R0,F0,F0)
        print(candKeys)
        for f in F0:
            lh=set(f.lh)
            rh=set(f.rh)
            if norm.checkBCNF(f,lh,rh,candKeys):
            #print(norm.FDListBCNF)
                break
        #print(norm.FDListBCNF)

        if not norm.FDListBCNF==[]:
            fd=norm.FDListBCNF[0]
            #print(fd)
            X=fd.lh
            #print(X)
            xclosure=F0.attribute_closure(X)
            #print(xclosure)
            R01=set(xclosure)
            #print(R01)
            R02=R0.copy()
            R02=R02.difference(R01)
            #print(R02)
            R02=R02.union(set(X))
            #print(R02)
            F01=self.projectFDs(R0,R01,F0)
            F02=self.projectFDs(R0,R02,F0)
            accum.append((R01,F01))
            self.decomposeBCNF(R02,F02,accum)
        else:
            accum.append((R0,F0))
        print("----End of Call----")
        return accum



    def projectFDs(self,ParentRelation,DecompRelation,ParentFDs):
        T=FDependencyList()
        properset=Normalization.findNonEmptySubsets(self,DecompRelation)
        for X in properset:
            xclosure=ParentFDs.attribute_closure(X)

            for a in xclosure:
                if DecompRelation.__contains__(a):
                    T.append(FDependency(list(X),list(a)))
        return T.MinimalCover()


    def addRelation(self,R1):

        """ This method will check if any of the currently
            added relation is a subset of New Relation """
        #check=False;
        T=self.List_Relation.copy()
        if self.List_Relation==[]:
            self.List_Relation.append(R1)
        else:
            for g in T:
                if(g.issubset(R1)):
                    self.List_Relation.remove(g)
                    #self.List_Relation.append(R1)

            self.List_Relation.append(R1)

        return 0
    def createNewRelation(self,nfd):

        g=list()
        g.extend(nfd.lh)
        g.extend(nfd.rh)

        return set(g)
    #N=Normalization ()
    def createKeyRelation(self,R,MinFDs,FDs):
        #KeyRelations=list()
        KeyRelations=Normalization.findCandKeys(self,R,MinFDs,FDs)
        return KeyRelations

    def candidateKeyChecking(self,R,MinFDs,FDs):
        flag=True
        keys=Normalization.findCandKeys(self,R,MinFDs,FDs)
        for R2 in self.List_Relation:
            for key in keys:
                if not key.issubset(R2):
                    flag=False
                else:
                    flag=True
        return flag
