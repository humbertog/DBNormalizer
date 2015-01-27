from DBNormalizer.model.SQLParser import *
from sqlalchemy import *

db = create_engine('postgresql://Gabriela:@localhost/Birdie')
insp = inspect(db)
# birdie.echo = True
meta = MetaData()
meta.reflect(bind=db)

db_schema = readDB_schema(insp)

print(db_schema.keys())
print(db_schema['buser'])
print(db_schema['buser'].get_attributes())
print(db_schema['buser'].get_attributes_type())
print(db_schema['buser'].get_attributes_autoincrement())
print(db_schema['buser'].get_attributes_nullable())
print(db_schema['buser'].get_attributes_default())
print(db_schema['buser'].get_attributes_type('username'))

