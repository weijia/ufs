import time
from localLibs.logSys.logSys import *
import collectionDatabaseBase as collectionDbBase

class objItemInCol:
    def __init__(self, idInCol, objUuid, timestamp):
        self.idInCol = idInCol
        self.objUuid = objUuid
        self.timestamp = timestamp
    def getIdInCol(self):
        return self.idInCol
    def getUuid(self):
        return self.objUuid
    def getTimestamp(self):
        return self.timestamp
        
class collectionOnMongoDbBase(collectionDbBase.collectionBaseInterface):
    '''
    {"collectionId": "folder://C:/", uuid:"xxxx-xxxx...", timestamp:xxxxx}
    '''
    def __init__(self, collectionId, mongoDbInst):
        ncl(type(mongoDbInst))
        self.collectionDb = mongoDbInst
        self.collectionId = unicode(collectionId)
        
    def getCollectionId(self):
        return self.collectionId
        
    def exists(self, idInCol):
        ncl("calling exists for :", [idInCol, self.collectionId])
        '''
        Check if idInCol exists in collection, it will not check if the object is updated
        '''
        if self.getObjUuidRaw(idInCol) is None:
            return False
        return True
    
    def getObjUuidRaw(self, idInCol):
        for i in self.collectionDb.find({"collectionId": self.collectionId, "idInCol":unicode(idInCol)
                               , "deleted":{"$exists": False}}).sort("timestamp", -1):
            ncl("item exists in collection:", i, idInCol, self.collectionId)
            return i["uuid"]
        
        ncl({"collectionId": self.collectionId, "idInCol":unicode(idInCol)})
        return None
    
    def getObjUuid(self, idInCol):
        res = self.getObjUuidRaw(idInCol)
        if res is None:
            cl("item not exists in collection:", idInCol, self.collectionId)
            raise "no"
            return None
        #raise "exception"
        return res
            
    def addObj(self, idInCol, objUuid):
        newObjInCollection = {"collectionId": self.collectionId, "idInCol": unicode(idInCol), 
                            "timestamp": time.time(), "uuid": objUuid}
        #Insert the new object
        self.collectionDb.insert(newObjInCollection, safe=True)
        

    def isSame(self, idInCol, newObjId):
        oldUuid = self.getObjUuidRaw(idInCol)
        #cl(oldUuid)
        if oldUuid == newObjId:
            return True
        else:
            return False
    def removeAll(self):
        #Remove all items in collection
        self.collectionDb.find_and_modify({"collectionId": self.collectionId, 
                                           "deleted" : {"$exists": False}}, 
                                          {"$set" : { "deleted": "deleted"}})
        '''
        for i in self.collectionDb.find({"collectionId": self.collectionId, "idInCol":unicode(idInCol)}):
            print i
        '''
    def remove(self, idInCol):
        #Remove all idInCol from collection
        ncl('removing:', idInCol)
        self.collectionDb.find_and_modify({"collectionId": self.collectionId, 
                                           "idInCol":unicode(idInCol), "deleted" : {"$exists": False}}, 
                                          {"$set" : { "deleted": "deleted"}})
        '''
        for i in self.collectionDb.find({"collectionId": self.collectionId, "idInCol":unicode(idInCol)}):
            print i
        '''
    def updateObjUuidRaw(self, idInCol, newObjId):
        '''
        This function do not check if the old obj exists to prevent loop call for syncFolderCollection
        '''
        newObjInCollection = {"collectionId": self.collectionId, "idInCol":unicode(idInCol), 
                            "timestamp": time.time(), "uuid":newObjId}
        ncl("update item in collection:" + str(newObjInCollection))
        
        #Remove all old objects before inserting
        #self.collectionDb.update( {"collectionId": self.collectionId, "idInCol":unicode(idInCol)}, 
        #                    { "$set" : { "collectionId": self.collectionId+", deleted"} } , False, True, safe = True)
        self.collectionDb.find_and_modify({"collectionId": self.collectionId, "idInCol":unicode(idInCol)}, {"$set" : { "deleted": "deleted"}})
                   
        #Insert the new object
        self.collectionDb.insert(newObjInCollection, safe=True)
        
    def updateObjUuid(self, idInCol, newObjId):
        if self.isSame(idInCol, newObjId):
            cl("no updates needed", idInCol, newObjId)
            raise 'no update needed'
        self.updateObjUuidRaw(idInCol, newObjId)
            
    def updateObjUuidIfNeeded(self, idInCol, newObjId):
        if self.isSame(idInCol, newObjId):
            cl("no updates needed", idInCol, newObjId)
            return
        self.updateObjUuidRaw(idInCol, newObjId)

    def enumObjs(self, timestamp = 0):
        ncl("enumering", {"collectionId": self.collectionId, "timestamp":{"$gt": timestamp}})
        for i in self.collectionDb.find({"collectionId": self.collectionId, "timestamp":{"$gt": timestamp}, 
                               "deleted":{"$exists": False}}).sort("timestamp", 1):
            ncl("Got:", i)
            yield objItemInCol(i["idInCol"], i["uuid"], i["timestamp"])
            
    def enumObjsInRange(self, start = 0, count = 100, timestamp = 0):
        ncl("enumering", {"collectionId": self.collectionId, "timestamp":{"$gt": timestamp}})
        for i in self.collectionDb.find({"collectionId": self.collectionId, "timestamp":{"$gt": timestamp}, 
                               "deleted":{"$exists": False}}).sort("timestamp", 1).skip(start).limit(count):
            ncl("Got:", i)
            yield objItemInCol(i["idInCol"], i["uuid"], i["timestamp"])