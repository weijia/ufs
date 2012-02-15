import libs.services.services

def getItemData():
    from libs.services.sysAttr import *
    s = libs.services.services.services()
    h = s.getHtmlGen()
    h.genTxtHead()
    #h.genHead()

    dbName = s.getParam('treeImporterDb','treeImporterDb')
    db = s.getSimpleDb(dbName)
    d = s.getParam('treeRoot', s.getDefaultTreeRoot())
    dataId = db.getAttr(d, sys_itemTextAttr)


    defaultStorageDbName = 'testStorageDb'

    storeDb = s.getStorage(s.getParam('store', defaultStorageDbName))
    print storeDb.getData(dataId),
    h.end()
    #h.genEnd()