import libs.services.services

from libs.services.sysAttr import *
s = libs.services.services.services()
h = s.getHtmlGen()
h.genBinHead()
#h.genHead()

dbName = s.getParam('treeImporterDb','treeImporterDb')
db = s.getSimpleDb(dbName)
dataId = s.getParam('storageId', None)

defaultStorageDbName = 'testStorageDb'

storeDb = s.getStorage(s.getParam('store', defaultStorageDbName))
#h.write('dataid is-------------------------------------------------------:'+dataId)
h.write(storeDb.getData(dataId))
#h.write('dataid is-------------------------------------------------------:'+dataId)
h.end()
#h.genEnd()