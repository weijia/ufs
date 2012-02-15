import libs.services.services

from libs.services.sysAttr import *
s = libs.services.services.services()
h = s.getHtmlGen()
h.genTxtHead()
#h.genHead()

dbName = s.getParam('treeImporterDb','treeImporterDb')
#db = s.getSimpleDb(dbName)
treeItemAbsPath = s.getParam('treeRoot', s.getDefaultTreeRoot())
#dataId = db.getAttr(d, sys_itemTextAttr)
sequenceDbName = s.getParam('treeImporterBigValueDb','treeImporterBigValueDb')
nameDbId = s.getParam('treeImporterNameDb','treeImporterNameDb')
i = s.getTreeItem(dbName, nameDbId, treeItemAbsPath, sequenceDbName)
dataId = i.getContainer()
print dataId,
h.end()
#h.genEnd()