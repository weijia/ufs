import localLibSys
#import desktopApp.onlineSync.folderStorageV3 as folderStorage
import wwjufsdatabase.libs.utils.objTools as objTools

from pymongo import Connection
import uuid
import time
from localLibs.logSys.logSys import *
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import wwjufsdatabase.libs.utils.transform as transform
import ufsObj

class ObjectDoesNotExistInLocalFileSystem: pass

'''
class objectDatabaseInterface:
    def __init__(self):
        pass
    def getCollection(self, collectionId):
        pass
    def getFsObj(self, objUrl):
        pass
    def getFsObjFromFullPath(self, fullPath):
        pass
'''
class objectDatabase:
    '''
    every item has uuid attribute. objUrl is not necessary.
    '''
    def __init__(self, userSession = None, dbPrefix = ""):
        connection = Connection()
        if userSession is None:
            self.user = None
            ncl("------------------------------- user session is None")
        else:
            self.user = unicode(userSession.getUserName())
        self.collectionDb = connection[dbPrefix + "objectCollectionDbV2"].posts
        self.objDb = connection[dbPrefix + "objectDbV2"].posts
        self.collectionDb.ensure_index("timestamp")
        self.collectionDb.ensure_index("uuid")
        self.collectionDb.ensure_index("headMd5")
        self.collectionDb.ensure_index("idInCol")
        self.collectionDb.ensure_index("deleted")
        self.objDb.ensure_index("timestamp")
        self.objDb.ensure_index("uuid")
        self.objDb.ensure_index("headMd5")
        self.objDb.ensure_index("objUrl")
        self.objDb.ensure_index("size")
        self.objDb.ensure_index("fullPath")
        
    def getObjFromUuid(self, objUuid):
        ncl('get obj from uuid:', objUuid)
        if type(objUuid) != unicode:
            print type(objUuid)
            raise 'error type'
        for i in self.objDb.find({"uuid":unicode(objUuid)}).sort("timestamp", -1):
            #Remove internal id
            del i["_id"]
            if not i.has_key("fullPath") and i.has_key("objUrl"):
                cl(i)
                i["fullPath"] = objTools.parseUrl(i["objUrl"])[1][1:]
            return i
        cl("no obj find for uuid:", objUuid)
        #raise "No obj found"
        return None
    ##################################################
    # The following function are not related to database and is utils function
    ##################################################
    def getFullPathFromUfsUrl(self, ufsUrl):
        ufsUrlObj = ufsObj.ufsUrlObj(ufsUrl)
        return ufsUrlObj["fullPath"]
        
    def getFsObjFromUfsUrl(self, ufsUrl):
        ufsUrlObj = ufsObj.ufsUrlObj(ufsUrl)
        return self.getFsObjFromFullPath(ufsUrlObj["fullPath"])
        
    def getFsObjFromUuid(self, objUuid):
        '''
        This will return the latest obj whose full path is specified by object with UUID=objUuid
        '''
        legacyObjInfo = self.getObjFromUuid(objUuid)
        fullPath = legacyObjInfo["fullPath"]
        obj = ufsObj.fsObj(fullPath, legacyObjInfo)
        #Check if the legacy object still exists
        if not obj.exists(fullPath):
            return None
        ncl('target obj:', legacyObjInfo)
        newObj = self.getFsObjFromFullPath(fullPath)
        return newObj
    
    def insertObj(self, objInfoDict):
        objInfoDict["uuid"] = unicode(str(uuid.uuid4()))
        objInfoDict["user"] = self.user
        #objInfoDict["ufsUrl"] = ufsUrl
        objInfoDict["addedTimestamp"] = time.time()
        ncl(objInfoDict)
        #####################
        # If the object is just a dictionary, it has no getItemInfo method
        #####################
        try:
            self.objDb.insert(objInfoDict.getItemInfo(), safe=True)
        except AttributeError:
            pass
        ncl(objInfoDict)
        if objInfoDict.has_key("_id"):
            del objInfoDict["_id"]
        ncl('returning new obj', objInfoDict["uuid"])
        ncl(objInfoDict)
        return objInfoDict
        
    def getFsContainerObjFromFullPath(self, fullPath):
        dirObjInFs = ufsObj.fsDirObj(fullPath)
        ufsUrl = dirObjInFs.getObjUfsUrl()
        if not dirObjInFs.exists():
            cl('obj does not exists', fullPath)
            raise ObjectDoesNotExistInLocalFileSystem()
            return None
        #cl('finding url:', ufsUrl)
        for i in self.objDb.find({"ufsUrl": ufsUrl}).sort("timestamp", -1):
            #Check if the item is updated
            if dirObjInFs["timestamp"] == i["timestamp"]:
                #Object time NOT changed, treated it as NOT changed.
                #cl("item not changed:", i)
                return ufsObj.ufsUrlObj(ufsUrl, i)
        #The item is updated add the new item
        latestInfo = dirObjInFs.getItemInfo()
        #dirObjInFs["uuid"] = unicode(str(uuid.uuid4()))
        #dirObjInFs["user"] = self.user
        dirObjInFs["ufsUrl"] = ufsUrl
        #dirObjInFs["addedTimestamp"] = time.time()
        #self.objDb.insert(dirObjInFs.getItemInfo(), safe=True)
        #ncl('returning new obj')
        #print objInFs["uuid"]
        return self.insertObj(dirObjInFs)
    
    def getFsObjFromFullPath(self, fullPath):
        '''
        Return object info with {"ufsUrl": "ufs://hostname/D:/tmp/xxx",
            "size": size, "timestamp": timestamp}
        '''
        objInFs = ufsObj.fsObj(fullPath)
        if objInFs.isContainer():
            res = self.getFsContainerObjFromFullPath(fullPath)
            ncl("returning: ", res["uuid"])
            return res
        ufsUrl = objInFs.getObjUfsUrl()
        if not objInFs.exists():
            ncl(fullPath)
            raise ObjectDoesNotExistInLocalFileSystem()
            return None
        for i in self.objDb.find({"ufsUrl": ufsUrl}).sort("timestamp", -1):
            #Check if the item is updated
            if objInFs["size"] == i["size"]:
                #Object size NOT changed
                if objInFs["timestamp"] == i["timestamp"]:
                    #Object size and time NOT changed, treated it as NOT changed.
                    del i["_id"]
                    ncl(i)
                    return ufsObj.ufsUrlObj(ufsUrl, i)
                if objInFs["headMd5"] == i["headMd5"]:
                    #The file is changed, but the content is not changed. Update the timestamp for the obj or add new item with new timestamp?
                    ncl('existing item as size and hash is the same, return existing info')
                    #Update the timestamp in the database as the item's timestamp in file system is different
                    self.objDb.find_and_modify({"uuid":i["uuid"]}, {"$set": {"timestamp":objInFs["timestamp"]}})
                    ncl("returnning: ", i["uuid"])
                    del i["_id"]
                    ncl(i)
                    return ufsObj.ufsUrlObj(ufsUrl, i)
        #The item is updated add the new item
        latestInfo = objInFs.getItemInfo()
        #objInFs["uuid"] = unicode(str(uuid.uuid4()))
        #objInFs["user"] = self.user
        objInFs["ufsUrl"] = ufsUrl
        #self.objDb.insert(objInFs.getItemInfo(), safe=True)
        #ncl('returning new obj')
        #print objInFs["uuid"]
        return self.insertObj(objInFs)

    def getFsObjUuid(self, objUrl):
        return self.getFsObj(objUrl)["uuid"]
        
        
    def getDbObj(self, objUrl):
        for i in self.objDb.find({"objUrl":unicode(objUrl)}).sort("timestamp", -1):
            #Remove internal id
            del i["_id"]
            return i
        return None
    def isUpdated(self, srcObjUuid, dstObjUuid):
        '''
        Check if srcObjUuid is newer than dstObjUuid
        '''
        if srcObjUuid == dstObjUuid:
            #Same object, ignore
            ncl('same obj')
            return False
        srcObj = self.getObjFromUuid(srcObjUuid)
        dstObj = self.getObjFromUuid(dstObjUuid)
        if (srcObj["size"] == dstObj["size"]):
            if srcObj["timestamp"] == dstObj["timestamp"]:
                return False
            if (srcObj["headMd5"] == dstObj["headMd5"]):
                ncl('equal obj')
                return False
        if srcObj["timestamp"] > dstObj["timestamp"]:
            cl('updated true')
            return True
        
    def addVirtualObj(self, contentDict):
        if contentDict.has_key("uuid"):
            existing = self.findObj(contentDict)
            if existing is None:
                print contentDict
                raise "uuid exist but not the same object"
            else:
                #Find same obj, return
                return contentDict["uuid"]
        #The following will be done in insert
        '''
        else:
            contentDict["uuid"] = unicode(str(uuid.uuid4()))
        '''
        if not contentDict.has_key("timestamp"):
            contentDict["timestamp"] = time.time()
        
        if not contentDict.has_key("virtualObj"):
            contentDict["virtualObj"]= True
        
        ncl(contentDict)
        #self.objDb.insert(contentDict, safe=True)
        #return contentDict["uuid"]
        res = self.insertObj(contentDict)
        return res["uuid"]
        

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
        if contentDict.has_key("addedTimestamp"):
            raise "addedTimestamp already exists"
        
        contentDict["addedTimestamp"] = time.time()
        #cl(contentDict)
        self.objDb.insert(contentDict, safe=True)
        #The following checks if the insert is OK
        '''
        flag = False
        for i in self.objDb.find(contentDict):
            cl('inserted obj:', i)
            flag = True
        if not flag:
            cl('------------------------------insert failed')
        '''
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
        '''
        if True:
            self.objDb.update( {"objUrl":unicode(objUrl)}, 
                            {"$set" : {"deleted":True}} , False, True, safe=True)#Here false means do not insert if the item does not exist, true means if multiple items, udpate all
        else:
            self.objDb.find_and_modify({"objUrl":unicode(objUrl)}, {"$set" : newValueDict})
            
    def updateObjByUuid(self, objUuid, newValueDict):
        self.objDb.find_and_modify({"uuid": unicode(objUuid)}, {"$set" : newValueDict})
        
    def getCollectionDb(self):
        return self.collectionDb
        
    def getCollection(self, collectionId):
        '''
        may be:
        folder://C:/
        '''
        return collectionDatabase.collectionOnMongoDbBase(collectionId, self.collectionDb)
        
def main():
    pass
    
     
if __name__ == '__main__':
    main()
