__author__ = 'Humberto, Gabriela'

from DBNormalizer.model.Relation import *
from sqlalchemy import *


def readDB_schema(db_inspector):
    db_schema = {}
    tables = db_inspector.get_table_names()

    for name in tables:
        att = db_inspector.get_columns(name)
        rel = Relation(name, att)
        db_schema[name] = rel

    return db_schema


