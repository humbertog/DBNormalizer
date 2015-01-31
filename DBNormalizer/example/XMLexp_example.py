__author__ = 'Paris'

from DBNormalizer.example.relations import readDB_schema
from DBNormalizer.model.SQLParser import *
from DBNormalizer.model.Decomp import *
from DBNormalizer.model.XMLIO import *

'''
The correct path to folder should be specified for exPath
'''
exPath="/Users/mariaslanova/PycharmProjects/DBNormalizer/DBNormalizer/DBNormalizer/XML/XML_export/"

N=Normalization()
D=Decomposition()
Xml=XmlParsing()
db = create_engine('postgresql://mariaslanova:@localhost/Test1')
insp = inspect(db)
meta = MetaData()
meta.reflect(bind=db)

relations_list = readDB_schema(insp)
names = list(relations_list.keys())
tabNo=0
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
        tabName="table"+str(tabNo)
        S=list();
        for s in l[1]:
            S.append((s.lh,s.rh))
        Xml.writeTableToXML(tabName,list(l[0]),S,"Decomposition",exPath)
        S.clear()
        tabNo=tabNo+1


    L.clear()



