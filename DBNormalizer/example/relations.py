__author__ = 'Nantes'
from DBNormalizer.model.Relation import *
from sqlalchemy import *


#db = create_engine('postgresql://humberto:@localhost/birdie')
#insp = inspect(db)
# birdie.echo = True
#meta = MetaData()
#meta.reflect(bind=db)
#
def readDB_schema(db_inspector):
    db_schema = {}
    tables = db_inspector.get_table_names()

    for name in tables:
        att = db_inspector.get_columns(name)
        pk = db_inspector.get_pk_constraint(name)
        unique = db_inspector.get_unique_constraints(name)
        rel = Relation(name, schema_attributes=att, schema_keys=pk, schema_unique=unique)
        db_schema[name] = rel

    return db_schema

#relations = readDB_schema(insp)
#print(relations['buser'])