__author__ = 'mariaslanova'

from DBNormalizer.example.relations import readDB_schema
from DBNormalizer.model.SQLParser import *
from DBNormalizer.model.Decomp import *

N=Normalization()
D=Decomposition()

db = create_engine('postgresql://humberto:@localhost/dbnormalizer_test')
insp = inspect(db)
meta = MetaData()
meta.reflect(bind=db)

relations_list = readDB_schema(insp)
names = list(relations_list.keys())

for i in range(0,len(names)):
    nam = names[i]
    #print(nam)
    partitions_dict = get_table_partitions(nam, relations_list[nam].attributes, db)
    #print(relations_list[nam].attributes)
    rltn = set(relations_list[nam].attributes)
    print('Relation = ',rltn)
    #print (nam,'=',set(relations_list[nam].attributes))
    relations_list[nam].find_fds(partitions_dict)
    FDS = (relations_list[nam].fds)
    #print(relations_list[nam])
    print('FDs = ',FDS)

    #FDs = FDependencyList([fd1, fd2, fd3, fd4,fd5])
    minFds=FDS.MinimalCover()
    print('MinCover = ',minFds)
    #allKeys = FDs.candidate_keys()
    allKeys=N.findCandKeys(rltn,minFds,FDS)
    print('Keys = ',allKeys)

    # for fd in minFds:
    #     lhs=set(fd.lh)
    #     rhs=set(fd.rh)

     #    if(N.check2NF(fd,lhs,rhs,allKeys)):
    #        print("2nf violation")
     #    if(N.check3NF(fd,lhs,rhs,allKeys)):
    #        print("3nf violation")
      #   if(N.checkBCNF(fd,lhs,rhs,allKeys)):
    #        print("BCNF violation")

    L=D.proposalBCNF(rltn,minFds)
    for l in L:
       print(l[0])
       print(l[1])
       print("\n")
    L.clear()