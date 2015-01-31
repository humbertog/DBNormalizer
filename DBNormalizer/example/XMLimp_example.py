__author__ = 'Paris'

from DBNormalizer.example.relations import readDB_schema
from DBNormalizer.model.SQLParser import *
from DBNormalizer.model.Decomp import *
from DBNormalizer.model.XMLIO import *

'''
The correct path to folder should be specified for imPath
'''
imPath="/Users/mariaslanova/PycharmProjects/DBNormalizer/DBNormalizer/DBNormalizer/XML/XML_import/"
N=Normalization()
D=Decomposition()
Xml=XmlParsing()
db = create_engine('postgresql://mariaslanova:@localhost/Test1')
insp = inspect(db)
meta = MetaData()
meta.reflect(bind=db)

tableinfo=Xml.readXMLToTable("table0.xml",imPath)
print(tableinfo['Table_Name'])

reltn=set(tableinfo['Column'])
print(reltn)
g=tableinfo['Dependency']
FDs=FDependencyList()
for t in g:
    FDs.append(FDependency(t[0],t[1]))
print(FDs)
