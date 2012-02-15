import time

class collectionInterface:
    def __init__(self, collectionId):
        self.collectionId = collectionId

    def exists(self, objUrl):
        return False
        
    def updated(self, objUrl):
        return False

    def updateObj(self, objUrl):
        pass
        
    def addVirtualObj(self, objUrl, newObjId):
        pass
        
    def enumObjInCollectionDb(self, timestamp = 0):
        pass
        
    def enumCollectionItem(self, timestamp = 0):
        pass
        
    def getObj(self, objUrl):
        pass
        
        
'''
class collectionDbBackendInterface:
    def findItem(self, itemRuleDict):
        pass
    

class collectionMongoDbBackEnd:
    def __init__(self, db):
        connection = Connection()
        if userSession is None:
            self.user = None
        else:
            self.user = unicode(userSession.getUserName())
        self.db = connection["objectCollectionDb"].posts
    def findItem(self, itemRuleDict, sort = -1):
        for i in self.db.find(itemRuleDict).sort("timestamp", sort):
            yield i
'''
            
class collectionBaseInterface:
    def exists(self, objUrl):
        pass
    def getObjUuid(self, objUrl):
        pass
    def addObj(self, objUrl, objUuid):
        pass
    def enumObjs(self, timestamp):
        pass
    def isSame(self, objUrl, newObjId):
        pass
    def updateObjUuid(self, objUrl, newObjId):
        pass
        
class collectionOnMongoDbBase:
    def __init__(self, collectionId, mongoDbInst):
        self.db = mongoDbInst
        self.collectionId = unicode(collectionId)
    def exists(self, objUrl):
        ncl("calling exists for :", [objUrl, self.collectionId])
        '''
        Check if objUrl exists in collection, it will not check if the object is updated
        '''
        if self.getObjUuid(objUrl) is None:
            return False
        return True
        
    def getObjUuid(self, objUrl):
        for i in self.db.find({"collectionId": self.collectionId, "objUrl":unicode(objUrl)}).sort("timestamp", -1):
            ncl("item exists in collection:", objUrl)
            return i
        return None
            
    def addObj(self, objUrl, objUuid):
        newObjInCollection = {"collectionId": self.collectionId, "objUrl":unicode(objUrl), 
                            "timestamp":time.time(), "uuid":newObjId}
        #Insert the new object
        self.db.collectionDb.insert(newObjInCollection, safe=True)
    def enumObjs(self, timestamp):
        ncl("enumering", {"collectionId": self.collectionId, "timestamp":{"$gt": timestamp}})
        for i in self.db.collectionDb.find({"collectionId": self.collectionId, "timestamp":{"$gt": timestamp}}).sort("timestamp", 1):
            ncl("Got:", i)
            yield i

    def isSame(self, objUrl, newObjId):
        oldUuid = self.getObjUuid(objUrl)
        if oldUuid == newObjId:
            return False
        else:
            return True
            
    def updateObjUuid(self, objUrl, newObjId):
        if self.isSame(objUrl, newObjId):
            print objUrl, newObjId
            raise 'no update needed'
            
        newObjInCollection = {"collectionId": self.collectionId, "objUrl":unicode(objUrl), 
                            "timestamp": time.time(), "uuid":newObjId}
        ncl("update item in collection:" + str(newObjInCollection))
        
        #Remove all old objects before inserting
        self.db.update( {"collectionId": self.collectionId, "objUrl":unicode(objUrl)}, 
                            { "$set" : { "collectionId": self.collectionId+", deleted"} } , False, True, safe = True)
                            
        #Insert the new object
        self.db.insert(newObjInCollection, safe=True)
'''
class objSys:
    def __init__(self, collectionId, mongoDbInst, objSysInst):
        self.objSysInst = objSysInst
        
    def getObj(self, objUuid):
        self.obj
'''
'''
-----------------------------------------------------
'''
class collectionCache(collectionInterface):
    def __init__(self, collectionId, collectionDbInst, originalCollection)
        self.collectionId = unicode(collectionId)
        self.collection = collectionOnMongoDbBase(collectionId, collectionDbInst)
        self.originalCollection = originalCollection

    def exists(self, objUrl):
        return self.collection.exists(objUrl)
        
    def isSame(self, objUrl):
        oldUuid = self.collection.getObjUuid(objUrl)
        originalUuid = originalCollection.getObjUuid(objUrl)
        if oldUuid == originalUuid:
            return True
        else:
            return False
            
    def updateObj(self, objUrl):
        if self.isSame(objUrl):
            print objUrl
            raise "don't need updateObj"
        self.collection.updateObjUuid(objUrl, self.originalCollection.getObjUuid(objUrl))
        


class collectionForSync(collectionCache):
    def __init__(self, collectionId, collectionDbInst, originalCollection, objectSys)
        collectionCache.__init__(self, collectionId, collectionDbInst, originalCollection)
        self.objectSys = objectSys

    def updated(self, objUrl):
        return self.isSame(objUrl)
        
    def getObj(self, objUrl):
        return self.objectSys.getObj(self.getObjUuid(objUrl))
    def addVirtualObj(self, objUrl, newObjId):
        self.collection.updateObjUuid(objUrl, newObjId)
        
    def enumCollectionItem(self, timestamp = 0):
        for i in self.collection.enumObjs(timestamp):
            yield i
        
