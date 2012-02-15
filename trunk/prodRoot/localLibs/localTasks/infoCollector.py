from stat import *
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
import os
class onlyFileElementHasFileSizeThisIsADir: pass
import localTaskInterfaces
'''
class sizeDb:
    def __init__(self, dbSysInst):
        self.dbSysInst = dbSysInst
    def getSize(self, item):
        itemSizeDb = self.dbSysInst.getDb("infoCollectionItemSize")
        sizeDb = self.dbSysInst.getDb("infoCollectionSizeDb")
        path = item.getCachedPath()
        itemId = item.getId()
        try:
            size = itemSizeDb[itemId]
            return size
        except KeyError:
            size = os.stat(path)[ST_SIZE]
            itemSizeDb[itemId] = unicode(str(size))
            #print 'adding:', itemId, unicode(str(size))
        try:
            elemList = sizeDb[unicode(str(size))]
        except KeyError:
            elemList = []
        if not (itemId in elemList):
            #print elemList
            sizeDb.append(unicode(str(size)), itemId)
            #print 'appending:',unicode(str(size)), itemId
        return size
    def getItemWithSize(self, size):
        import localLibs.cache.localFileSystemCache as localFileSystemCache
        cacheSys = localFileSystemCache.localFileSystemCache(self.dbInst)
        try:
            idList = sizeDb[unicode(str(size))]
        except KeyError:
            idList = []
        res = []
        for i in idList:
            res.append(cacheSys.getCached(self.fullPath))
        return res
'''

gHeadMd5Length = 1024

def getHeadContentMd5(fullPath):
    try:
        f = open(fullPath, 'rb')
    except IOError:
        #print "can not read", fullPath
        raise IOError
        return 0
    import md5
    data = f.read(gHeadMd5Length)
    '''
    p = "d:/tmp/a.xls"
    while os.path.exists(p):
        p = p+"t"
    wf = open(p, 'wb')
    wf.write(data)
    wf.close()
    '''
    res = unicode(md5.new(data).hexdigest())
    f.close()
    return res
        
def getSizeFromFs(fullPath):
    return unicode(str(os.stat(fullPath)[ST_SIZE]))
        
class InfoDb:
    def __init__(self, dbSysInst, infoGetter = getSizeFromFs, infoName = "sizeInfo"):
        self.dbSysInst = dbSysInst
        self.infoName = infoName
        self.infoGetter = infoGetter
    def getInfo(self, item):
        itemSizeDb = self.dbSysInst.getDb(self.infoName)
        #The mongo database do not support "." in key. So use _reverse instead of .reverse
        sizeDb = self.dbSysInst.getDb(self.infoName+"_reverse")
        path = item.getCachedPath()
        itemId = item.getId()
        #print 'get itemId:',itemId
        try:
            size = itemSizeDb[itemId][0]
            return size
        except KeyError:
            size = self.infoGetter(path)
            itemSizeDb[itemId] = size
            #print 'adding:', itemId, unicode(str(size))
        try:
            elemList = sizeDb[unicode(str(size))]
            #print 'got element with the same size,',elemList
        except KeyError:
            elemList = []
        #print "item Id: %s for %s, size: %s, same:%s"%(itemId,path,size,'.'.join(elemList))
        if not (itemId in elemList):
            #print elemList
            sizeDb.append(unicode(str(size)), itemId)
            #print 'appending:',unicode(str(size)), itemId
        return size
    def getItemWithInfo(self, size):
        #print 'checking size:',size
        import localLibs.cache.localFileSystemCache as localFileSystemCache
        #The mongo database do not support "." in key. So use _reverse instead of .reverse
        sizeDb = self.dbSysInst.getDb(self.infoName+"_reverse")
        cacheSys = localFileSystemCache.localFileSystemCache(self.dbSysInst)
        try:
            idList = sizeDb[unicode(str(size))]
            #print 'same size id list:', idList
        except KeyError:
            idList = []
            #print 'no item found'
        res = []
        #print idList
        for i in idList:
            res.append(cacheSys.getCached(i))
        return res

        
class fileSizeProcessor:
    def process(self, item, dbInst):
        sizeDb(dbInst).getSize(item)
        
    
class localPathElement(localTaskInterfaces.elementInterface):
    def __init__(self, fullPath, dbInst):
        #if os.path.isdir(fullPath):
        #    raise onlyFileElementHasFileSizeThisIsADir()
        self.fullPath = fullPath
        self.dbInst = dbInst
    def getCachedPath(self):
        return transform.transformDirToInternal(self.fullPath)
    def getId(self):
        import localLibs.cache.localFileSystemCache as localFileSystemCache
        cacheSys = localFileSystemCache.localFileSystemCache(self.dbInst)
        return cacheSys.getObjId(self.fullPath)

        
if __name__=='__main__':
    import localLibs.test.testDbSys as testDbSys
    d = testDbSys.testDbSys()
    l = localPathElement("H:\\Need to check\\6120c_4061.sisx", d)
    processElement(l, d)
    itemSizeDb = d.getDb("infoCollectionItemSize")
    sizeDb = d.getDb("infoCollectionSizeDb")
    size = itemSizeDb[l.getId()]
    print size
    print sizeDb[unicode(str(size[0]))]