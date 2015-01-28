__author__ = 'Nantes'

from DBNormalizer.example.relations import readDB_schema
from DBNormalizer.model.SQLParser import *
#postgresql://user:password@localhost/mydatabase
db = create_engine('postgresql://Gabriela:@localhost/Test')
insp = inspect(db)
meta = MetaData()
meta.reflect(bind=db)

relations_list = readDB_schema(insp)
names = list(relations_list.keys())

for i in range(0,len(names)):
    nam = names[i]
    partitions_dict = get_table_partitions(nam, relations_list[nam].attributes, db)
    relations_list[nam].find_fds(partitions_dict)
    print(relations_list[nam])
