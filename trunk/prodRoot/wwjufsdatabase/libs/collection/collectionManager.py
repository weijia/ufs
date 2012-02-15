import libSys
import libs.ufs.ufsTreeItem as ufsTreeItem
import libs.collection.collectionBase as collectionBase
import libs.utils.objTools as objTools
import collectionInterface
import libs.utils.configurationTools as configurationTools

def getOriginalCollectionId(collectionId, dbSysInst):
    return dbSysInst.originalCollectionDb()[collectionId]

class undefinedCollection:pass

def getCollectionByProtocol(collectionId, dbSysInst):
    moduleName, itemUrl = collectionId.split(configurationTools.getFsProtocolSeparator(),2)
    collectionModule = __import__("libs.collection.modules."+moduleName, globals(),locals(),["getCollection"], -1)
    return collectionModule.getCollection(itemUrl, dbSysInst)




def getCollection(collectionId, dbSysInst, folderOnly = False):
    '''
    The basic algrithom for this function is:
    1. Find the original collection for the collectionId represented collection
    2. Update the collectionId represented collection if possible
    3. return the latest collection snapshot for the original collection
    So we can always get the latest snapshot for the original collection
    '''
    #If the collection is an uuid, for example: uuid://xxxx-xxxxxxxx-xxxx-xxxx-xxxx,
    #then get the local cache for that object. If no local cache for the object, return the collection directly
    if objTools.isUuid(collectionId) or objTools.isUfsFs(collectionId):
        #it is uuid://xxxxx or is ufsFs://xxxx
        id = objTools.getUuid(collectionId)
        #It's a UUID
        try:
            import localLibs.cache.localFileSystemCache as localFileSystemCache
            try:
                cacheSys = localFileSystemCache.localFileSystemCache(dbSysInst)
                cachedPath = cacheSys.getCached(id)
            except KeyError:
                cachedPath = None
        except ImportError:
            cachedPath = None
        if cachedPath is None:
            #No local path exist, return the collection directly
            return collectionBase.collectionBase(collectionId, dbSysInst.getCollectionDb())
    elif objTools.isUfsUrl(collectionId):
        #It is not uuid://xxx and not ufsFs:xxx, but in other ufs url format like xxxx://xxxxxx
        return getCollectionByProtocol(collectionId, dbSysInst)
    else:
        #The collectionID is not in uuid://xxxx-xxxx-xxxx format. Treat it as a path.
        cachedPath = collectionId
    #Either it is an ID that pointed to a local filesystem collection or treat it as a directory
    try:
        #print 'create new cache'
        import localLibSys
        import localLibs.collection.fileSystem.fileSystemCollection as fileSystemCollection
        import cachedCollection
        try:
            f = fileSystemCollection.fileSystemCollection(cachedPath, folderOnly)
        except fileSystemCollection.pathNotExist:
            return collectionBase.collectionBase(collectionId, dbSysInst.getCollectionDb())
        except fileSystemCollection.pathIsNotCollection:
            #print 'pathIsNotCollection, it seems to be a file', collectionId.encode('gbk', 'replace')
            return collectionInterface.emptyCollection()
        c = cachedCollection.simpleCacheCollection(dbSysInst, f)
        #print '----------------------------------'
        #print c
        return c
    except ImportError:
        pass
    raise undefinedCollection
        
def main():
    import libs.ufsDb.dbSys as dbSys
    co = getCollection('C:/', dbSys.dbSysSmart(), False).getRange(0, None)
    print co
    for i in co:
        print i,",is empty?",getCollection(i, dbSys.dbSysSmart(), False).isEmpty()
    
if __name__=='__main__':
    main()