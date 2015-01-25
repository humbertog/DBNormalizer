__author__= 'Humberto''Gabriela'


from sqlalchemy import *

db = create_engine('postgresql://Gabriela:@localhost/Birdie')
insp = inspect(db)
# birdie.echo = True
meta = MetaData()
meta.reflect(bind=db)

tables = insp.get_table_names()
a = tables[3]

def read_attributes(insp, name):
    attributes = []
    attributes_db = insp.get_columns(name)
    for j in attributes_db:
         attributes.append(j['name'])
    return attributes

#def read_adom(insp,name):
#    adom = []


print(read_attributes(insp, a))
print(insp.get_columns(a))

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