__author__ ='Paris'


from DBNormalizer.model.Decomp import *

N=Normalization()
D=Decomposition()
RO=set(['A','B','C','D','E'])

fd1 = FDependency(['A','B'],['C'])
fd2 = FDependency(['B'],['D'])
fd3 = FDependency(['A','B','E'],['C','D'])
fd4 = FDependency(['C','D'],['E'])
fd5 = FDependency(['C','E'],['A'])
# fd1 = FDependency(['A', 'B'], ['C','D'])
# fd2 = FDependency(['A'], ['B'])
# fd3 = FDependency(['B'], ['C'])
# fd4 = FDependency(['C'], ['E'])
# fd5 = FDependency(['B', 'D'], ['A'])
    # fd6 = FDependency(['C', 'D'], ['E'])
    # fd7 = FDependency(['A', 'C'], ['B'])
    # fd8 = FDependency(['A', 'C'], ['D'])
    # fd9 = FDependency(['A', 'C'], ['E'])
    # fd10 = FDependency(['C'], ['A'])
FDs = FDependencyList([fd1, fd2, fd3, fd4,fd5])
minFds=FDs.MinimalCover()
print(minFds)
    #allKeys = FDs.candidate_keys()
allKeys=N.findCandKeys(RO,minFds,FDs)
print(allKeys)

# for fd in minFds:
#     lhs=set(fd.lh)
#     rhs=set(fd.rh)
#
#     if(N.check2NF(fd,lhs,rhs,allKeys)):
#         print("2nf violation")
#     if(N.check3NF(fd,lhs,rhs,allKeys)):
#         print("3nf violation")
#     if(N.checkBCNF(fd,lhs,rhs,allKeys)):
#         print("BCNF violation")

print(N.FDListBCNF)
L=D.proposalBCNF(RO,minFds)
for l in L:
    print(l[0])
    print(l[1])
    print("\n")
