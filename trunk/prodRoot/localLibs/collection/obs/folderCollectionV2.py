import localLibSys
import desktopApp.onlineSync.folderStorageV3 as folderStorage
import localLibs.collection.objectDatabaseV2 as objectDatabase
import os
import wwjufsdatabase.libs.utils.misc as misc
from localLibs.logSys.logSys import *

class folderStorageStateOnDb:
    def __init__(self, collectionId):
        '''
        collectionId is the local state for all objects in the folder storage
        '''
        self.db = objectDatabase.objectDatabase()
        self.collection = self.db.getCollection(collectionId)
    def updated(self, item):
        ncl(item.itemInfo)
        newObjUuid = self.db.getFsObj(item.getItemObjUrl())["uuid"]
        return self.collection.isSame(item.getItemObjUrl(), newObjUuid)
    def update(self, item):
        '''
        Update local collection info, replace object url to local path?
        '''
        remoteInfo = item.getItemInfo()
        if remoteInfo.has_key("objUrl"):
            remoteInfo["encZipStorageUrl"] = remoteInfo["objUrl"]
            del remoteInfo["objUrl"]
        if remoteInfo.has_key("uuid"):
            remoteInfo["encZipStorageUuid"] = remoteInfo["uuid"]
            del remoteInfo["uuid"]
        #print remoteInfo["encZipStorageUrl"]
        itemUuid = self.db.addDbObj(item.getItemObjUrl(), remoteInfo)
        ncl(remoteInfo)
        ncl(itemUuid)
        self.collection.updateObjUuid(item.getItemObjUrl(), itemUuid)
        
    def updateLocal(self, item):
        itemUuid = self.db.getFsObj(unicode(item.getItemObjUrl()))["uuid"]
        self.collection.updateObjUuid(item.getItemObjUrl(), itemUuid)
        
    def getItemState(self, item):
        ncl(item.getItemObjUrl())
        objUuid = self.collection.getObjUuid(item.getItemObjUrl())
        res = self.db.getDbObj(objUuid)
        ncl("returnning", res)
        return res
        
        
class folderCollection:
    def __init__(self, rootDir, backupDir, collectionId):
        self.rootDir = rootDir
        self.backupDir = backupDir
        self.lastState = folderStorageStateOnDb(collectionId)
        self.db = objectDatabase.objectDatabase()
    def store(self, item, pendingCollection):
        
        #Check if the item in folder storage is newer than the target one
        relaPath = item.getRelaPath()
        localFullPath = os.path.join(self.rootDir, relaPath)
        localPathDir = os.path.dirname(localFullPath)
        localItem = folderStorage.folderStorageItem(self.rootDir, localFullPath)
        extItem = folderStorage.externalItem(self.rootDir, localFullPath, item.getItemInfo())
        #This item stores the item info in local collection. It will be used to check 
        #if the item is changed after the last write from external storage
        info = self.lastState.getItemState(localItem)
        if info is None:
            info = {}
        extItemLocalCopy = folderStorage.folderStorageItem(self.rootDir, localFullPath, info)

        if (not os.path.exists(localFullPath)):
            cl('item does not exist, add it')
            #Copy the updated file to local path
            misc.ensureDir(localPathDir)
            item.saveTo(self.rootDir)
            #Check if the timestamp are updated
            if localItem.getTimestamp() != extItem.timestamp():
                raise 'not work as expected, need to manually update time for local copy'
            self.lastState.update(extItem)
        elif self.lastState.updated(localItem):
            ncl('item updated, check it')
            if extItemLocalCopy.isExternal():
                ncl("External obj")
                #It is an external file, check time
                if (extItemLocalCopy.getExtTs() < item.getTimestamp()):
                    ncl("External storage has updated the item, update the local one")
                    #External storage has updated the item, update the local one
                    backupFullPath = fileTools.getFreeNameFromFullPath(os.path.join(self.backupDir, relaPath))
                    backupPathDir = os.path.dirname(backupFullPath)
                    misc.ensureDir(backupPathDir)            
                    shutil.move(localFullPath, backupFullPath)
                    #Copy the updated file to local path
                    misc.ensureDir(localPathDir)
                    item.saveTo(self.rootDir)
                    self.lastState.update(extItem)
            else:
                if extItemLocalCopy.getTimestamp() < item.getTimestamp():
                    #External storage has updated the item, update the local one
                    cl(extItemLocalCopy.getTimestamp() , item.getTimestamp())
                    backupFullPath = fileTools.getFreeNameFromFullPath(os.path.join(self.backupDir, relaPath))
                    backupPathDir = os.path.dirname(backupFullPath)
                    misc.ensureDir(backupPathDir)            
                    shutil.move(localFullPath, backupFullPath)
                    #Copy the updated file to local path
                    misc.ensureDir(localPathDir)
                    item.saveTo(self.rootDir)
                    self.lastState.update(extItem)
                else:
                    ncl("The item need to be stored is not newer than the local one, the info for local item will be updated")
                    self.lastState.updateLocal(localItem)