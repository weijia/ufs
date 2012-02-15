import localLibSys
import wwjufsdatabase.libs.ufsDb.dbSysInterface as dbSysInterface
import localLibs.localDb.sqliteListShoveWithHistory as shove

import os

try:#if True:#try:
    import libs.GAE.ufsDbGaeListShove as shove
    #import libs.GAE.ufsDbGaeShove as shove
except ImportError:#else:#except ImportError:
    import sys
    c = os.getcwd()
    while c.find('prodRoot') != -1:
      c = os.path.dirname(c)
    #print c
    sys.path.insert(0, os.path.join(c,'prodRoot'))
    #import localLibs.localDb.sqliteAttrDb.sqliteEntryDbWithHistory as entryDbMod
    #import localLibs.localDb.sqliteAttrDb.sqliteTokenDb as tokenDbMod
    import localLibs.localDb.shoveInDefaultPath as shove
    #gAppPath = 'd:/tmp/fileman/'
    #gDbPath = os.path.join(gAppPath, 'db')
    #import libs.utils.misc as misc
    #import libs.ufsDb.ufsDbBase as ufsDbBase
    #misc.ensureDir(gAppPath)
    #misc.ensureDir(gDbPath)

gAppPath = 'd:/tmp/test/'
gDbPath = os.path.join(gAppPath, 'db')
import wwjufsdatabase.libs.utils.misc as misc
misc.ensureDir(gAppPath)
misc.ensureDir(gDbPath)


class testDbSys(dbSysInterface.dbSysInterface):
    def __init__(self, sessionInstance = None):
        self.sessInst = sessionInstance
    def getObjId2PathShove(self):
        return self.getDb("objId2PathShove")
    def getPath2ObjIdShove(self):
        return self.getDb("path2ObjIdShove")
    def getCollectionCacheIdDb(self):
        return self.getDb("collectionCacheIdDb")
    def getCollectionCacheUpdateDb(self):
        return self.getDb("collectionCacheUpdateDb")
    def getCollectionCacheDb(self):
        return self.getDb("collectionCacheDb")
    def getCollectionDb(self):
        return self.getDb("collectionDb")
    def getNameServiceDb(self):
        return self.getDb("nameServiceDb")
    def getOriginalCollectionDb(self):
        return self.getDb("originalCollectionDb")
    def getDbForTag(self, tagDbName):
        return self.getDb(tagDbName)
    def getDb(self, dbName):
        db = shove.ShoveForSession(dbName, self.sessInst, gDbPath)
        import libs.shove.encryptedListShove as encShove
        return encShove.ShoveLike(db)
