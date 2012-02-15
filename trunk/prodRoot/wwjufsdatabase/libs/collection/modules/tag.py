import libSys
import libs.tag.objSystemIntegratedTagSystem as tagSys
import libs.tag.tagSystemV2 as baseTagSys
import libs.collection.collectionContainer as collectionContainer


def getCollection(url, dbSysInst):
    t = tagSys.tagSystemShoveDb(dbSysInst)
    notUsed, tagValue = url.split(t.getExcludedTagPrefix(),2)
    '''
    print tagValue.encode('gbk', 'replace')
    return collectionContainer.collectionContainerWrapperForPythonList([tagValue])
    '''
    paths = baseTagSys.tagSystemShoveDb.getObjs(t, t.getExcludedTagStr(tagValue))
    taggedList = t.getAllObjects(tagValue)
    '''
    for i in t.enumObjsWithTag(tagValue):
        #print i
        taggedList.append(i)
    '''
    taggedCollection = collectionContainer.collectionContainerWrapperForPythonList(taggedList)
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