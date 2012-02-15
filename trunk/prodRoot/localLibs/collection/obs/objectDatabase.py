import localLibSys
import desktopApp.onlineSync.folderStorageV3 as folderStorage
import wwjufsdatabase.libs.utils.objTools as objTools
import UserDict
from pymongo import Connection
import uuid
import time
from localLibs.logSys.logSys import *


class objectDatabaseInterface:
    def __init__(self):
        pass
    def getCollection(self, collectionId):
        pass
    def getFsObj(self, objUrl):
        pass
        
class collectionInterface:
    def __init__(self, collectionId = None):
        self.collectionId = collectionId
    def exists(self, itemUrl):
        pass
    def updateObj(self, objUrl):
        pass

    
        
class fsObj(UserDict.DictMixin, folderStorage.objBase):
    def __init__(self, fullPath, existingItemInfo = {}):
        folderStorage.objBase.__init__(self, fullPath, existingItemInfo)
        self.itemInfo["fullPath"] = self.fullPath
        
    def __getitem__(self, key):
        ncl(str(self.itemInfo))
        if self.itemInfo.has_key(key):
            return self.itemInfo[key]
        funcAttr = getattr(self, key)
        value = funcAttr()
        self.itemInfo[key] = value
        return value

    def __setitem__(self, key, value):
        self.itemInfo[key] = value
        return value

    def __delitem__(self, key):
        pass
    
    def keys(self):
        return self.itemInfo.keys()
        
class ufsObj(fsObj):
    def __init__(self, objUrl, existingItemInfo = {}):
        self.objUrl = objUrl
        objPath = objTools.parseUrl(objUrl)[1][1:]
        ncl('ufsObj fullPath:', objPath)
        fsObj.__init__(self, objPath, existingItemInfo)
        

class collection(collectionInterface):
    def __init__(self, db, collectionId):
        self.db = db
        self.collectionId = collectionId

    def exists(self, objUrl):
        ncl("calling exists for :", [objUrl, self.collectionId])
        '''
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId)}).sort("timestamp", -1):
            cl(i)
        '''
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl)}).sort("timestamp", -1):
            ncl("item exists in collection:", objUrl)
            return True
        return False
    def updated(self, objUrl):
        '''
        if self.collectionId is None:
            return False
        '''
        res = None
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl)}).sort("timestamp", -1):
            res = i
            ncl('find obj:',i)
        if res is None:
            #Object is not in the collection, so need update
            ncl('object is not in collection', {"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl)})
            '''
            for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId)}).sort("timestamp", -1):
                cl("\n"+i["objUrl"]+"\n"+objUrl)
            '''
            return True
        if res["uuid"] == self.db.getFsObj(unicode(objUrl))["uuid"]:
            return False
        else:
            return True

    def updateObj(self, objUrl):
        '''
        prevObjs = []
        #Get all previous objects, so we can remove them later
        for i in self.objDb.find({"collectionId":self.collectionId, "objUrl":objUrl}).sort("timestamp", -1):
            prevObjs.append(i)
        '''
        objItem = self.db.getFsObj(unicode(objUrl))
        ncl(objItem)
        newObjId = objItem["uuid"]
        
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl),
                                            "uuid":newObjId}).sort("timestamp", -1):
            cl("!!!!!!!item exists in collection:", objUrl)
            return
        
        newObjInCollection = {"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl), 
                            "timestamp":time.time(), "uuid":newObjId}
        ncl("Add item in collection:" + str(newObjInCollection))
        #Remove all old objects before inserting
        self.db.collectionDb.update( {"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl)}, 
                            { "$set" : { "collectionId":self.collectionId+", deleted"} } , False, True)
        #Insert the new object
        self.db.collectionDb.insert(newObjInCollection, safe=True)
        
    def addVirtualObj(self, objUrl, newObjId):
        newObjInCollection = {"collectionId":unicode(self.collectionId), "objUrl":unicode(objUrl), 
                            "timestamp":time.time(), "uuid":newObjId}
        #Insert the new object
        self.db.collectionDb.insert(newObjInCollection, safe=True)
        
    def enumObjInCollectionDb(self, timestamp = 0):
        ncl("enumering", {"collectionId":unicode(self.collectionId), "timestamp":{"$gt": timestamp}})
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId), "timestamp":{"$gt": timestamp}}).sort("timestamp", 1):
            cl("Got:", i)
            yield self.db.getDbObj(i["objUrl"])
    def enumCollectionItem(self, timestamp = 0):
        ncl("enumering", {"collectionId":unicode(self.collectionId), "timestamp":{"$gt": timestamp}})
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId), "timestamp":{"$gt": timestamp}}).sort("timestamp", 1):
            ncl("Got:", i)
            yield i
    def getObj(self, objUrl):
        for i in self.db.collectionDb.find({"collectionId":unicode(self.collectionId), "objUrl":objUrl}).sort("timestamp", 1):
            ncl("Got:", i)
            return self.db.findObj({u"uuid":i["uuid"]})
        return None
        
class objectDatabase:
    def __init__(self, userSession = None):
        connection = Connection()
        if userSession is None:
            self.user = None
        else:
            self.user = unicode(userSession.getUserName())
        self.collectionDb = connection["objectCollectionDb"].posts
        self.objDb = connection["objectDb"].posts
        
    def getCollection(self, collectionId):
        '''
        #Check if collectionId exists
        for i in self.collectionDb.find({"collectionId":collectionId,"user":self.user}):
            #CollectionId exists, so return a collection with the id set
            return collection(self, collectionId)
        '''
        return collection(self, unicode(collectionId))


    def getFsObj(self, objUrl):
        ncl('getting: ', objUrl)
        #Find the latest item
        objInFs = ufsObj(unicode(objUrl))
        for i in self.objDb.find({"objUrl":unicode(objUrl)}).sort("timestamp", -1):
            ncl("comparing timestamp", objInFs["timestamp"], i["timestamp"])
            #Check if the item is updated
            ncl(i)
            if objInFs["timestamp"] == i["timestamp"]:
                ncl("got existing obj uuid:"+ufsObj(unicode(objUrl), i)["uuid"])
                return ufsObj(unicode(objUrl), i)
            ncl("comparing timestamp", objInFs["size"], i["size"])
            if objInFs["size"] == i["size"]:
                if objInFs["headMd5"] == objInFs["headMd5"]:
                    #The file is changed, but the content is not changed. Update the timestamp for the obj or add new item with new timestamp?
                    ncl('existing item as size and hash is the same, return existing info')
                    ncl(ufsObj(unicode(objUrl), i)["uuid"])
                    #Update the timestamp
                    self.objDb.update({"uuid":i["uuid"]}, {"timestamp":objInFs["timestamp"]}, False, True)
                    return ufsObj(unicode(objUrl), i)
        #The item is updated add the new item
        latestInfo = objInFs.getItemInfo()
        objInFs["uuid"] = unicode(str(uuid.uuid4()))
        objInFs["user"] = self.user
        objInFs["objUrl"] = unicode(objUrl)
        self.objDb.insert(objInFs.getItemInfo(), safe=True)
        ncl('returning new obj')
        #print objInFs["uuid"]
        return objInFs
        
    def getDbObj(self, objUrl):
        for i in self.objDb.find({"objUrl":unicode(objUrl)}).sort("timestamp", -1):
            #Remove internal id
            del i["_id"]
            return i
        return None
    def addDbObj(self, objUrl, contentDict):
        #######################
        #TODO: remove old obj with the same objUrl?
        '''
        for i in ["objUrl", "uuid"]:
            if contentDict.has_key(i):
                #print contentDict
                raise 'system field can not be used as attribute'
        '''
        if contentDict.has_key("objUrl"):
            if objUrl != contentDict["objUrl"]:
                print objUrl, contentDict["objUrl"]
                raise "objUrl is not equal"
        else:
            contentDict["objUrl"] = unicode(objUrl)

        if contentDict.has_key("uuid"):
            existing = self.findObj(contentDict)
            if existing is None:
                print contentDict
                raise "uuid exist but not the same object"
        else:
            contentDict["uuid"] = unicode(str(uuid.uuid4()))
            
        if not contentDict.has_key("timestamp"):
            contentDict["timestamp"] = time.time()
        #cl(contentDict)
        self.objDb.insert(contentDict, safe=True)
        flag = False
        for i in self.objDb.find(contentDict):
            cl('inserted obj:', i)
            flag = True
        if not flag:
            cl('------------------------------insert failed')
        return contentDict["uuid"]

    def findObj(self, objDict):
        ncl(objDict)
        for i in self.objDb.find(objDict).sort("timestamp", -1):
            return i
        return None
    def updateObj(self, objUrl, newValueDict):
        '''
        cl(objUrl, newValueDict)
        newV = {"nextToProcess": newValueDict["nextToProcess"]}
        #for i in newValueDict:
        for i in self.objDb.find({"objUrl":unicode(objUrl)}):
            cl(i, newValueDict)
        '''
        '''
        #Remove all old objects before inserting
        self.objDb.update( {"objUrl":unicode(objUrl)}, 
                            {"$set" : newV} , False, True, safe=True)#Here false means do not insert if the item does not exist, true means if multiple items, udpate all
        '''
        self.objDb.find_and_modify({"objUrl":unicode(objUrl)}, {"$set" : newValueDict})
        
    def getCollectionDb(self):
        return self.collectionDb
        
def main():
    pass
    
     
if __name__ == '__main__':
    main()
