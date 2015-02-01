__author__ = 'Nantes'

from DBNormalizer.example.relations import readDB_schema
from DBNormalizer.model.SQLParser import *
from DBNormalizer.model.Decomp import *
from DBNormalizer.model.Relation import *


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


# Lets try to compute NF:
for nam in names:
    relations_list[nam].set_canonical_cover()
    relations_list[nam].set_candidate_keys()
    relations_list[nam].set_normalization()
    print("----------------------------")
    print(relations_list[nam])

print("=======================")

dec = Decomposition()
decomposition_dic = {}
for name in relations_list.keys():
    rel = relations_list[name]
    attr = rel.attributes
    canonical_cover = rel.canonical_cover

    # Decomposition proposal:
    dec_proposal = dec.proposalBCNF(set(attr), canonical_cover)
    # Saves the decomposition in a dictionary:
    decomposition_dic[name] = {}
    i = 1
    for tup in dec_proposal:
        sub_name = name + '_' + str(i)
        new_attr = list(tup[0])
        new_fds = FDependencyList(tup[1])
        new_relation = rel.sub_relation(sub_name, new_attr, new_fds)
        new_relation.set_canonical_cover()
        new_relation.set_candidate_keys()
        new_relation.set_normalization()
        decomposition_dic[name][sub_name] = new_relation
        i += 1


print(relations_list[name])
print(decomposition_dic['employee_project']['employee_project_1'])
print(decomposition_dic['employee_project']['employee_project_2'])
