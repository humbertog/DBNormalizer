__author__ = 'Paris'

from xml.etree import ElementTree as XmlTree
#import FDependency

#import FDependencyList
#import Relation
#fileHandler=open(path+filename,'r')


class XmlParsing:
    def __init__(self,Path=None,fileName=None, ):
        self.fileName=fileName
        self.Path=Path

        pass

    def writeTableToXML(self,tableName,attributeList,fdList,schemaName,exPath='/'):
        '''
        fdList is list of tuples of list of left and right hand fd
        fdList=[(['a','b'],['c']),([].[])....]
        '''
        XmlRoot=XmlTree.Element('configuration')
        Schema=XmlTree.SubElement(XmlRoot,'schema',{'name':schemaName})
        TableInfo=XmlTree.SubElement(Schema,"tableInfo")
        Table=XmlTree.SubElement(TableInfo,"table",{'name':tableName})
        attributes=XmlTree.SubElement(Table,"attributes")
        fds=XmlTree.SubElement(Table,"fds")
        for att in attributeList:
            at=XmlTree.SubElement(attributes,"attribute")
            at.text=att
        for fd in fdList:
            felem=XmlTree.SubElement(fds,"fd")
            lh=fd[0] #fd.lh
            rh=fd[1] #fd.rh
            lhs=XmlTree.SubElement(felem,"LHS")
            rhs=XmlTree.SubElement(felem,"RHS")
            for la in lh:
                lat=XmlTree.SubElement(lhs,"attribute")
                lat.text=la
            for ra in rh:
                rat=XmlTree.SubElement(rhs,"attribute")
                rat.text=ra
        Xtree=XmlTree.ElementTree(XmlRoot)

        Xtree.write(exPath+tableName+".xml")
        return 0
    def readXMLToTable(self,fileName,pathName="/"):
        TableInfo=dict()
        Tree=XmlTree.parse(open(pathName+fileName,'r'))
        treeRoot=Tree.getroot()
        #print(treeRoot.tag)
        schemaName=treeRoot[0].attrib['name']
        tables=treeRoot.findall(".//schema/tableInfo/table")
        #for table in tables:
        table=tables[0]
        tableName=table.attrib['name']
        attributes=table.findall("./attributes/attribute")
        #attributes=table.findall("./attributes/attribute")
        attList=list()
        for elem in attributes:
            attList.append(elem.text)
        #print("The attributes are:=",attList)
        FDs=table.findall("./fds/fd")
        #FdList=FDependencylist()
        FdList=list()
        #print(FDs)
        for fd in FDs:
            lhs=[l.text for l in fd.findall("./LHS/attribute")]
            rhs=[r.text for r in fd.findall("./RHS/attribute")]
            FdList.append((lhs,rhs))


        TableInfo['Schema_Name']=schemaName
        TableInfo['Table_Name']=tableName

        TableInfo['Column']=attList
        TableInfo['Dependency']=FdList

        return TableInfo










