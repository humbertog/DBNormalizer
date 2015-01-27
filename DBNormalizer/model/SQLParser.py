__author__ = 'Humberto, Gabriela'

from sqlalchemy import *


def get_schema_attribute_property(attr_schema, att_property='type', attr_name=None):
    attributes = []
    if attr_name is None:
        for x in attr_schema:
            attributes.append(x[att_property])
    else:
        attributes = [x[att_property] for x in self.attributes if x['name'] == attr_name]
    return attributes


def get_schema_keys(key_schema, key_property='constrained_columns'):
    return key_schema[key_property]


def get_schema_unique(unique_schema, un_property='column_names'):
    unique = []
    for x in unique_schema:
        unique.append(x[un_property])
    return unique


def get_table_partitions(table, attributes):
    partitions = {}
    attr = len(attributes)
    for i in range(attr):
        partitions[attributes[i]] = get_attribute_partition(table, attributes[i])
    return partitions


def get_attribute_partition(table, attribute, db):
    query = "select " + attribute + "," + " array_agg(index) as e from (select " + attribute + ","  \
            "row_number() over() as index from " + table + ") as fool  group by " + attribute
    execute = db.execute(query)
    x = []
    for row in execute:
        x.append(row['e'])
    return x
