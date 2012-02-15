import libSys
import libs.tag.multiUserTagSystem as tagSys
import libs.tag.tagSystemV2 as baseTagSys
import libs.collection.collectionContainer as collectionContainer


def getCollection(url, dbSysInst):
    listRes = ['good', 'bad']
    collectionContainer.collectionContainerWrapperForPythonList(listRes)
    return collectionContainer.collectionContainer(taggedCollection, dbSysInst)
    
    
def main():
    import libs.ufsDb.dbSys as dbSys
    dbSysInst = dbSys.dbSysSmart()
    a = ",\xc4\xe3\xba\xc3"#This is gbk encode of nihao. just input chinese nihao in python console, you will get this
    b = a.decode("gbk")
    print b
    c = getCollection(b, dbSysInst)
    for i in c.getRange(0, 50):
        print i
    
    
if __name__=='__main__':
    main()