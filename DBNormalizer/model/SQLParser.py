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


def get_table_partitions(table, attributes):
    partitions = {}
    attr = len(attributes)
    for i in range(attr):
        partitions[attributes[i]] = get_attribute_partition(table, attributes[i])
    return partitions


def get_attribute_partition(table, attribute):
    query = "select " + attribute + "," + " array_agg(index) as e from (select " + attribute + ","  \
            "row_number() over() as index from " + table + ") as fool  group by " + attribute
    execute = db.execute(query)
    x = []
    for row in execute:
        x.append(row['e'])
    return x
