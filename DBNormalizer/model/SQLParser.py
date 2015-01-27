__author__= 'Humberto''Gabriela'

from DBNormalizer.model.Relation import *
from DBNormalizer.model.FDependencyList import *
from sqlalchemy import *

db = create_engine('postgresql://Gabriela:@localhost/Birdie')
insp = inspect(db)
# birdie.echo = True
meta = MetaData()
meta.reflect(bind=db)

def readDB_schema(db_inspector):
    db_schema = {}
    tables = db_inspector.get_table_names()

    for name in tables:
        att = insp.get_columns(name)
        rel = Relation(name, att)
        db_schema[name] = rel

    return db_schema

db_schema = readDB_schema(insp)
#
# print(db_schema.keys())
# print(db_schema['buser'])
# print(db_schema['buser'].get_attributes())
# print(db_schema['buser'].get_attributes_type())
# print(db_schema['buser'].get_attributes_autoincrement())
# print(db_schema['buser'].get_attributes_nullable())
# print(db_schema['buser'].get_attributes_default())
# print(db_schema['buser'].get_attributes_type('username'))
#

fd1 = FDependency(['A'], ['C', 'D']) # means A -> CD
fd2 = FDependency(['B'], ['C'])
fd3 = FDependency(['C', 'D'], ['E'])

# Instantiate an object that contains a list of FDs:
fds1 = FDependencyList([fd1,fd2, fd3])
print(fds1.attribute_closure(['A','B']))


def check_fds(lhs,rhs,fds):
    closure = fds.attribute_closure(lhs)
    return rhs[0] in closure


print(check_fds(['A','B'], ['E'], fds1))

def get_lhs_rhs(lhs,rhs,e0,e1,fds):
    lhs

def get_lhs_rhs(lhs, rhs, e0, e1, fds):
    lhs_set = set(lhs)
    e1_sub = [i for i in e1 if set(i).issubset(set(lhs))]
    e1_sub.sort(key=len, reverse=True)
    x = lhs
    for k in e1_sub:
        x = list(set(x) - set(k))
    x = list(set(x) - set(e0))

    while x.__len__() != 0:
        if check_fds(x, rhs, fds):
            e1.append(x)
            x.pop()
        else:
            e0 = list()



    print(x)

get_lhs_rhs(['A', 'B','C','D','E'], [], [], [['B', 'C'], ['D'], ['A','B','C']],[])



def get_fds(attribute, db_engine=0):
    lhs = attribute[:]
    len = attribute.__len__()
    for i in range(1,len):
        rhs = lhs.pop()


