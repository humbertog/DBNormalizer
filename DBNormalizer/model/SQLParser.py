__author__ = 'Humberto, Gabriela'

from sqlalchemy import *


def get_schema_attribute_property(attr_schema, att_property='type', attr_name=None):
    attributes = []
    if attr_name is None:
        for x in attr_schema:
            attributes.append(x[att_property])
    else:
        attributes = [x[att_property] for x in attributes if x['name'] == attr_name]
    return attributes


def get_schema_keys(key_schema, key_property='constrained_columns'):
    return key_schema[key_property]


def get_schema_unique(unique_schema, un_property='column_names'):
    unique = []
    for x in unique_schema:
        unique.append(x[un_property])
    return unique


def get_table_partitions(table, attributes, db):
    partitions = {}
    attr = len(attributes)
    for i in range(attr):
        partitions[attributes[i]] = get_attribute_partition(table, attributes[i],db)
    return partitions


def get_attribute_partition(table, attribute, db):
    query = "select " + attribute + "," + " array_agg(index) as e from (select " + attribute + ","  \
            "row_number() over() as index from " + table + ") as fool  group by " + attribute
    execute = db.execute(query)
    x = []
    for row in execute:
        x.append(row['e'])
    return x

def parse_table(name, metadata, column_schema_list=None, pk_schema=None, unique_schema=None):
    table = Table(name, metadata)

    # Adds columns
    if column_schema_list:
        for k in column_schema_list:
            col = parse_column(k)
            table.append_column(col)

    # Adds primary key
    if pk_schema:
        pk = PrimaryKeyConstraint(*pk_schema['constrained_columns'], name=pk_schema['name'])
        table.append_constraint(pk)

    # Adds unique constrain
    if unique_schema:
        for k in unique_schema:
            unique = UniqueConstraint(*k['column_names'], name=k['name'])
            table.append_constraint(unique)

    return table


def parse_column(column_schema, primary_key=False, unique=False):
    name = column_schema['name']
    default = column_schema['default']
    c_type = column_schema['type']
    nullable = column_schema['nullable']
    autoincrement = column_schema['autoincrement']
    return Column(name, c_type, default=default, nullable=nullable, autoincrement=autoincrement,
                  primary_key=primary_key, unique=unique)


def decompose_schema_attributes(schema, over_attributes):
    new_schema = [x for x in schema if x['name'] in over_attributes]
    return new_schema


def decompose_schema_unique(schema, over_attributes):
    new_schema = [x for x in schema if set(x['column_names']).issubset(set(over_attributes))]
    return new_schema


def decompose_schema_pk(schema, over_attributes):
    if set(schema['constrained_columns']).issubset(set(over_attributes)):
        new_schema = schema
    else:
        new_schema = {}
    return new_schema