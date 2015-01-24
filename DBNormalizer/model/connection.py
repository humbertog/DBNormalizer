
from sqlalchemy import *
#from sqlalchemy.engine import reflection
#postgresql://user:password@localhost/mydatabase
birdie = create_engine('postgresql://Gabriela:@localhost/Birdie')
insp = inspect(birdie)
#birdie.echo = True
meta = MetaData()
meta.reflect(bind=birdie)
users_table = meta.tables['follower']

#print(insp.get_columns('follower'))
#print(insp.get_primary_keys('follower'))
#print(insp.get_schema_names())



tables2 = insp.get_table_names()

for i in tables2:
    print(i)
    cols=insp.get_columns(i)
    for j in cols:
        print(j['name'])
    print(insp.get_pk_constraint(i))
    print(insp.get_foreign_keys(i))

# e!