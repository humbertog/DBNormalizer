__author__ = 'Nantes'

from DBNormalizer.example.relations import readDB_schema
from DBNormalizer.model.SQLParser import *


#postgresql://user:password@localhost/mydatabase
db = create_engine('postgresql://humberto:@localhost/dbnormalizer_test')
insp = inspect(db)
meta = MetaData()
meta.reflect(bind=db)

relations_list = readDB_schema(insp)
names = list(relations_list.keys())

for i in range(0,len(names)):
    nam = names[i]
    partitions_dict = get_table_partitions(nam, relations_list[nam].attributes, db)
    relations_list[nam].find_fds(partitions_dict)
#    print(partitions_dict)
    #print(relations_list[nam])

print(relations_list)

print("=======================")
# Lets try to compute NF:
for nam in names:
    relations_list[nam].set_canonical_cover()
    relations_list[nam].set_candidate_keys()
    relations_list[nam].set_normalization()
    print("----------------------------")
    print(relations_list[nam])

