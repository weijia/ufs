import localLibSys
import wwjufsdatabase.libs.ufsDb.dbSys as dbSys
import wwjufsdatabase.libs.tag.inheritableExclusableTagSystem as tagSystem
import infoCollector
import wwjufsdatabase.libs.collection.collectionManager as collectionManager
import wwjufsdatabase.libs.tag.tagSystemV2 as baseTagSys

def tagChildElemExpandHandler(fullPath, handler, taskId, excluded = []):
    d = dbSys.dbSysSmart()
    e = infoCollector.localPathElement(fullPath, d)
    #print 'excluded:',excluded
    if e in excluded:
        return
    db = d.getDb('processedDb')
    if db.hasValue(taskId, e.getId()):
        #print 'processed--------------------------', fullPath.encode('gbk','replace')
        return
    #print taskId, e.getId(), fullPath.encode('gbk','replace')
    print 'processing:', fullPath.encode('gbk','replace')
    #Process the element first
    handler.process(e, d)
    #Process the child elements
    for i in collectionManager.getCollection(e.getCachedPath(), d).getRange(0, None):
        #print i.encode('gbk','replace')
        if i in excluded:
            continue
        tagChildElemExpandHandler(i, handler, taskId, excluded)
    db.append(taskId, e.getId())
    #print 'added:',taskId, e.getId(), fullPath.encode('gbk','replace')


def processTag(tag, handler = infoCollector.fileSizeProcessor(), taskId = u'908fde4b-7729-43b0-bff2-73d5e47d8836'):
    t = tagSystem.tagSystemShoveDb()
    d = dbSys.dbSysSmart()
    paths = baseTagSys.tagSystemShoveDb.getObjs(t, t.getExcludedTagStr(tag))
    for i in t.enumObjsWithTag(tag):
        tagChildElemExpandHandler(i, handler, taskId, paths)



if __name__=='__main__':
    #import localLibs.test.testDbSys as testDbSys
    #d = testDbSys.testDbSys()
    #l = localPathElement("H:\\Need to check\\6120c_4061.sisx", d)
    processTag(u"arrange")
    '''
    processElement(l, d)
    itemSizeDb = d.getDb("infoCollectionItemSize")
    sizeDb = d.getDb("infoCollectionSizeDb")
    size = itemSizeDb[l.getId()]
    print size
    print sizeDb[unicode(str(size[0]))]
    '''