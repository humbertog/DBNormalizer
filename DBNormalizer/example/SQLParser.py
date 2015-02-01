__author__ = 'Nantes'

from DBNormalizer.model.Relation import *
from sqlalchemy import *
from sqlalchemy.schema import CreateTable

# This function read the whole DB and returns a dictionary where the keys are the relation names
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


# Create connection to DB
# The db used in this example is the one Gabriela sent in skype
db = create_engine('postgresql://Gabriela:@localhost/Test')
meta = MetaData()
meta.reflect(bind=db)
# This thing read the whole schema this is the base to create the Relation objects
insp = inspect(db)

# Call to the function defined above
relations = readDB_schema(insp)
# Creates a meta2 object to store the Table constructions
meta2 = MetaData()
t1 = relations['department'].SQL_statement(meta2)
t2 = relations['dependent'].SQL_statement(meta2)
t3 = relations['employee_project'].SQL_statement(meta2)

# Print create table statements:
# NOTE: for some reason it is not working with point datatype in posgreSQL
print(CreateTable(t1))
print(CreateTable(t2))
print(CreateTable(t3))
# This will try to write in the database (now is not working as no engine is binded to meta2)
# meta2.create_all()

# A subrelation of a relation. The sub-relation is obtained from the attributes that are passed to this function:
# Read the Relation function as more capabilities are needed.
t3_sub = relations['employee_project'].sub_relation('employee_project_new', ['ssn', 'superssn', 'plocation'])
# Print relation object
print(t3_sub)
# Print query of new relation object
print(CreateTable(t3_sub.SQL_statement(meta2)))



