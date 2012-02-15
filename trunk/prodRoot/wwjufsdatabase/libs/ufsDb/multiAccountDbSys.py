import multiAccountDb as shove

class dbSysSmart:
    def __init__(self, primaryUser, secondaryUsers, dbSys):
        self.dbSys = dbSys
        self.primaryUser = primaryUser
        self.secondaryUsers = secondaryUsers
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
        return shove.ShoveForSession(dbName, self.primaryUser, self.secondaryUsers, self.dbSys)