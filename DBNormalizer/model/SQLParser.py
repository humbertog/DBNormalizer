__author__= 'Humberto''Gabriela'

from DBNormalizer.model.Relation import *
from sqlalchemy import *

db = create_engine('postgresql://humberto:@localhost/birdie')
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

print(db_schema.keys())
print(db_schema['buser'])
print(db_schema['buser'].get_attributes())
print(db_schema['buser'].get_attributes_type())
print(db_schema['buser'].get_attributes_autoincrement())
print(db_schema['buser'].get_attributes_nullable())
print(db_schema['buser'].get_attributes_default())
print(db_schema['buser'].get_attributes_type('username'))



def read_attributes(insp, name):
    attributes = []
    attributes_db = insp.get_columns(name)
    for j in attributes_db:
         attributes.append(j['name'])
    return attributes

#def read_adom(insp,name):
#    adom = []



<<<<<<< HEAD

print(read_attributes(insp, a))
print(insp.get_columns(a))
=======
>>>>>>> FETCH_HEAD

# print(tables)
# for i in tables:
#     print(i)
#     cols = insp.get_columns(i)
#     for j in cols:
#         print(j['name'])
#     print(insp.get_pk_constraint(i))
#     print(insp.get_foreign_keys(i))
#
# FDs = db.execute("SELECT leftAttributes, count(*)"
#                  " FROM (select distinct leftAttributes, rightAttributes FROM tables) as  "
#                  "group by leftAttributes having count(*)>1")