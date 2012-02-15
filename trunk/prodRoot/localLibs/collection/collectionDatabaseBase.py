import UserDict

'''
class collectionInterface:
    def __init__(self, collectionId):
        self.collectionId = collectionId

    def exists(self, objUrl):
        return False
        
    def updateObj(self, objUrl):
        pass
        
    def enumCollectionItem(self, timestamp = 0):
        pass
        
    def getObj(self, objUrl):
        pass
        
'''
            
class collectionBaseInterface(UserDict.DictMixin):
    def __getitem__(self, objUrl):
        return self.getObjUuid(objUrl)

    def __setitem__(self, objUrl, newObjId):
        if self.exists(objUrl):
            return self.updateObjUuid(objUrl, newObjId)
        else:
            return self.addObj(objUrl, newObjId)

    def __delitem__(self, objUrl):
        self.remove(objUrl)
    
    def keys(self):
        print "keys not supported"
        raise "not supported"
        
    def has_key(self, objUrl):
        return self.exists(objUrl)
    
    ####################################
    #Subclass should implements the following methods.
    ####################################
    def exists(self, objUrl):
        pass
    def getObjUuid(self, objUrl):
        pass
    def addObj(self, objUrl, objUuid):
        pass
    def remove(self, objUrl):
        pass
    def enumObjs(self, timestamp):
        pass
    def isSame(self, objUrl, newObjId):
        pass
    def updateObjUuid(self, objUrl, newObjId):
        pass