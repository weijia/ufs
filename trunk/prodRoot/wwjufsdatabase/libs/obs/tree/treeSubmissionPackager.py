import libSys
import libs.utils.objTools as objTools
import os
import libs.ufs.ufs as ufs


def packageTreePath(collectionId, dbSysInst, dictElem):
    if objTools.isUuid(collectionId):
        id = objTools.getUuid(collectionId)
        #It's a UUID
        import localLibs.cache.localFileSystemCache as localFileSystemCache
        cacheSys = localFileSystemCache.localFileSystemCache(dbSysInst)
        cachedPath = cacheSys.getCached(id)
    elif objTools.isUfsUrl(collectionId):
        protocol,cachedPath = objTools.parseUrl(collectionId)
    else:
        cachedPath = collectionId
    parent = None
    while True:
        parent = os.path.dirname(os.path.abspath(cachedPath))
        #print parent, cachedPath
        if os.path.abspath(parent) == os.path.abspath(cachedPath):
            #Root dir, return root item
            dictElem[objTools.getUfsLocalRootUrl()] = objTools.getUfsUrl(cachedPath)
            dictElem[ufs.getUfsUuidItemUrl()] = objTools.getUfsLocalRootUrl()
            break
        dictElem[objTools.getUfsUrl(parent)] = objTools.getUfsUrl(cachedPath)
        cachedPath = parent

    
def main():
    import localLibSys
    import localLibs.test.testDbSys as testDbSys
    res = {}
    d = testDbSys.testDbSys()
    packageTreePath("d:/tmp/", d, res)
    print res
    
    
if __name__=='__main__':
    main()