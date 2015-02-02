__author__ = 'Nantes-Paris'

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


def get_duplicate_colums(table, lhs, rhs, conn):
    #TODO Not IMPLEMENTED
    lhs_c = lhs[:]
    rhs_c = rhs[:]
    left_attr = lhs_c.pop(0)
    right_att = rhs_c.pop(0)
    for i in lhs_c:
        left_attr = over + "," + i

    for i in rhs_c:
        right_att = over + "," + i

    query =  "select" + left_attr + ", count(*) from (select distinct " + left_attr + "," + right_att + \
             "from" + table + "group by" + left_attr + "having count(*) > 1"

    return query


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


"""
Argument "table" should be an object of class table, argument
"db" should be an instance of create_engine().
autocommit parameter should be TRUE
"""
def Create_Table(table,db):
    table.metadata.create(db)

"""
Following methods replicates method Create_Table() but output is directed onto a .sql file
instead of database
"""
def Create_Table_File(table):
    from sqlalchemy.schema import CreateTable
    filename = table.name + ".sql"
    f = open(filename,'w+')
    f.write(CreateTable(table.metadata))
    f.close()


"""
Arguments "main_table and subsume_of_main_tabletable" should be an object of class table,
argument "db" should be an instance of create_engine(), "over_attributes" are the list of attributes
that will be copied from main_table onto the subsume_of_main_tabletable.
autocommit parameter should be TRUE
"""
def Copy_data(main_table,subsume_of_main_table,over_attributes,db):
    query = "SELECT " + over_attributes + " FROM " + main_table.name
    temp = db.execute(query)
    for row in temp:
        query = "INSERT INTO " + subsume_of_main_table.name + " VALUES(" + row +")"
        db.execute(query)

"""
Following methods replicates method Copy_data() but output is directed onto a .sql file
instead of database
"""
def Copy_data_file(main_table,subsume_of_main_table,over_attributes,db):
    query = "SELECT " + over_attributes + " FROM " + main_table.name
    temp = db.execute(query)
    filename = subsume_of_main_table.name + ".sql"
    f = open(filename,'a+')
    for row in temp:
        query = "INSERT INTO " + subsume_of_main_table.name + " VALUES(" + row +")"
        f.write("\n")
        f.write(query)
    f.close()

"""
Argument "table" should be an object of class table, argument
"db" should be an instance of create_engine().
autocommit parameter should be TRUE
"""
def Drop_table(table,db):
    query = "DROP TABLE IF EXISTS " +table.name
    db.execute(query)


"""
Following methods replicates method Drop_table() but output is directed onto a .sql file
instead of database
"""
def Drop_table_file(table):
    query = "DROP TABLE IF EXISTS " +table.name
    filename = table.name + ".sql"
    f = open(filename,'a+')
    f.write("\n")
    f.write(query)
    f.close()
