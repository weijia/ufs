import localLibSys
import desktopApp.onlineSync.folderStorageV3 as folderStorage
import wwjufsdatabase.libs.utils.objTools as objTools
import UserDict
from pymongo import Connection
import uuid
import time
from localLibs.logSys.logSys import *
import collectionDatabaseV2 as collectionDatabase
import wwjufsdatabase.libs.utils.transform as transform
import copy
import os
import localLibs.localTasks.infoCollector as infoCollector

class objectDatabaseInterface:
    def __init__(self):
        pass
    def getCollection(self, collectionId):
        pass
    def getFsObj(self, objUrl):
        pass

        
       
class objBase(UserDict.DictMixin):
    def __init__(self, existingItemInfo = {}):
        self.itemInfo = copy.copy(existingItemInfo)
        
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
        
    def getItemInfo(self):
        return self.itemInfo

class fsObjBase(objBase):
    def __init__(self, fullPath, existingItemInfo = {}):
        self.fullPath = transform.transformDirToInternal(fullPath)
        self.itemInfo = copy.copy(existingItemInfo)
        self.itemInfo["fullPath"] = self.fullPath
        
    def exists(self):
        return os.path.exists(self.fullPath)
    #########################################################
    #The following methods are for dict
    #########################################################
    def itemAttr(self, key):
        if self.itemInfo.has_key(key):
            #print 'has key:', key
            return self.itemInfo[key]
        else:
            #print 'calling func:', key
            self.itemInfo[key] = getattr(self, key)()
            return self.itemInfo[key]
        
    def fillInfo(self, attrName):
        res = {}
        for i in attrName:
            res[i] = self.itemAttr(i)
        return res
        
    def size(self):
        #print '%s size: %d'%(self.fullPath, os.stat(self.fullPath).st_size)
        return os.stat(self.fullPath).st_size
    
    def timestamp(self):
        return os.stat(self.fullPath).st_mtime
    
    def headMd5(self):
        #raise "generating md5"
        ncl("Generating Md5")
        return infoCollector.getHeadContentMd5(self.fullPath)
        
    def getItemInfo(self):
        tmp = self.fillInfo(["timestamp", "fullPath", "headMd5", "size"])
        return self.itemInfo
    
    def getItemObjUrl(self):
        return self.getObjUrl()
    
    def getObjUrl(self):
        return u"file:///"+self.fullPath

class fsObj(fsObjBase): pass
        
class ufsObj(fsObj):
    def __init__(self, objUrl, existingItemInfo = {}):
        self.objUrl = objUrl
        objPath = objTools.parseUrl(objUrl)[1][1:]
        ncl('ufsObj fullPath:', objPath)
        fsObj.__init__(self, objPath, existingItemInfo)
        
class objInCollection(fsObjBase):
    def __init__(self, idInCol, itemInfo):
        objBase.__init__(self, itemInfo)
        self.itemInfo["idInCol"] = transform.formatRelativePath(idInCol)
        
    def getIdInCol(self):
        return self.itemInfo["idInCol"]

class objectDatabase:
    '''
    every item has uuid attribute. objUrl is not necessary.
    '''
    def __init__(self, userSession = None, dbPrefix = ""):
        connection = Connection()
        if userSession is None:
            self.user = None
        else:
            self.user = unicode(userSession.getUserName())
        self.collectionDb = connection[dbPrefix + "objectCollectionDb"].posts
        self.objDb = connection[dbPrefix + "objectDb"].posts
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
    def getFsObjFromUuid(self, objUuid):
        obj = self.getObjFromUuid(objUuid)
        ncl('target obj:', obj)
        newObj = fsObjBase(obj["fullPath"])
        if not newObj.exists():
            return None
        objUrl = newObj.getItemObjUrl()
        ncl(objUrl)
        return self.getFsObj(objUrl)
        
    def getFsObj(self, objUrl):
        '''
        objUrl is an real URL (with protocol://xxxxxxxxx format)
        '''
        ncl('getting: ', objUrl)
        #Find the latest item
        objInFs = ufsObj(unicode(objUrl))
        if not objInFs.exists():
            return None
        if os.path.isdir(objInFs["fullPath"]):
            return None
        for i in self.objDb.find({"objUrl":unicode(objUrl)}).sort("timestamp", -1):
            ncl("comparing timestamp", objInFs["timestamp"], i["timestamp"])
            #Check if the item is updated
            ncl('objinfo in db:', i)
            ncl("comparing size", objInFs["size"], i["size"])
            if objInFs["size"] == i["size"]:
                if objInFs["timestamp"] == i["timestamp"]:
                    ncl("got existing obj uuid:"+ufsObj(unicode(objUrl), i)["uuid"])
                    return ufsObj(unicode(objUrl), i)
                if objInFs["headMd5"] == i["headMd5"]:
                    #The file is changed, but the content is not changed. Update the timestamp for the obj or add new item with new timestamp?
                    cl('existing item as size and hash is the same, return existing info')
                    ncl(ufsObj(unicode(objUrl), i)["uuid"])
                    #Update the timestamp in the database as the item's timestamp in file system is different
                    #self.objDb.update({"uuid":i["uuid"]}, {"timestamp":objInFs["timestamp"]}, False, True, safe=True)
                    self.objDb.find_and_modify({"uuid":i["uuid"]}, {"$set": {"timestamp":objInFs["timestamp"]}})
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
            contentDict["uuid"] = unicode(str(uuid.uuid4()))

        if not contentDict.has_key("timestamp"):
            contentDict["timestamp"] = time.time()
        
        if not contentDict.has_key("virtualObj"):
            contentDict["virtualObj"]= True
        
        ncl(contentDict)
        self.objDb.insert(contentDict, safe=True)
        return contentDict["uuid"]

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
        self.objDb.find_and_modify({"uuid":unicode(objUuid)}, {"$set" : newValueDict})
        
    def getCollectionDb(self):
        return self.collectionDb
        
    def getCollection(self, collectionId):
        return collectionDatabase.collectionOnMongoDbBase(collectionId, self.collectionDb)
        
def main():
    pass
    
     
if __name__ == '__main__':
    main()
