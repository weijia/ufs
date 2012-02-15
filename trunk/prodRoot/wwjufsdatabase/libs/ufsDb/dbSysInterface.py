

class dbSysInterface:
    def getObjId2PathShove(self):
        pass
    def getPath2ObjIdShove(self):
        pass
    def getCollectionCacheIdDb(self):
        pass
    def getCollectionCacheUpdateDb(self):
        pass
    def getCollectionCacheDb(self):
        pass
    def getCollectionDb(self):
        '''
        Used by collection manager
        '''
        return self.getCollectionCacheDb()
