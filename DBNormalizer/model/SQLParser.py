


from sqlalchemy import *


def dbconnection(db):
    DB = create_engine('postgresql://Gabriela:@localhost/Birdie')
    insp = inspect(DB)
    # birdie.echo = True
    meta = MetaData()
    meta.reflect(bind=DB)
    tables = insp.get_table_names()
    for i in tables:
        print(i)
        cols=insp.get_columns(i)
        for j in cols:
            print(j['name'])
        print(insp.get_pk_constraint(i))
        print(insp.get_foreign_keys(i))


