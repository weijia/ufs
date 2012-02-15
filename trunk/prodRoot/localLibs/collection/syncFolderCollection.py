import localLibSys
#import desktopApp.onlineSync.folderStorageV3 as folderStorage
import localLibs.objSys.ufsObj as ufsObj
import os
import wwjufsdatabase.libs.utils.misc as misc
from localLibs.logSys.logSys import *
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import synchronizableCollection
import shutil
import wwjufsdatabase.libs.utils.fileTools as fileTools
import copy
import wwjufsdatabase.libs.utils.transform as transform
import folderRecursiveEnumCollection as folderRecursiveEnumCollection

class syncFolderItem(ufsObj.objInCollection):
    def __init__(self, rootPath, itemInfo):
        self.rootPath = transform.transformDirToInternal(rootPath)
        self.fullPath = transform.transformDirToInternal(itemInfo["fullPath"])
        relaPath = transform.formatRelativePath(self.fullPath.replace(self.rootPath, ''))
        super(syncFolderItem, self).__init__(relaPath, itemInfo)

    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    def getItemInfo(self):
        tmp = self.fillInfo(["timestamp", "fullPath", "headMd5", "size"])
        return self.itemInfo



class syncFolderCollection(collectionDatabase.collectionOnMongoDbBase, 
                           synchronizableCollection.synchronizableCollection):
    
    def __init__(self, rootDir, backupDir, syncFolderCollectionId, dbInst):
        '''
        syncFolderCollectionId is a virtual collection which contains all items with synced info
        '''
        collectionDatabase.collectionOnMongoDbBase.__init__(self, syncFolderCollectionId, dbInst.getCollectionDb())
        self.rootDir = transform.transformDirToInternal(rootDir)
        self.backupDir = transform.transformDirToInternal(backupDir)
        self.objDb = dbInst
        self.folderCollection = folderRecursiveEnumCollection.folderRecursiveEnumCollection(self.rootDir, dbInst)

            
            
    #############################################
    # The following methods are called externally
    #############################################
    
    #############################################
    # The following methods are called when this collection is source collection
    #############################################
    def exists(self, idInCol):
        '''
        This function is called in sync to check if the object exists
        in sync collection to check if the item still exists 
        '''
        return self.folderCollection.exists(idInCol)

    
    def enumObjs(self, timestamp = 0):
        for i in self.folderCollection.enumObjs(timestamp):
            idInCol = i.getIdInCol()
            srcObjUuid = self.folderCollection.getObjUuid(idInCol)
            if collectionDatabase.collectionOnMongoDbBase.exists(self, idInCol):
                dstObjUuid = collectionDatabase.collectionOnMongoDbBase.getObjUuid(self, idInCol)
                ncl('dest uuid:', dstObjUuid, 'src:', srcObjUuid)
                if not self.objDb.isUpdated(srcObjUuid, dstObjUuid):
                    ncl("item not updated after extraction, ignore", idInCol)
                    continue
            cl('item updated after extraction, return it')
            yield i
    
    #############################################
    # The following methods are called when this collection are both src and dest
    # Called by archiver? only?
    #############################################    
    def getObjUuid(self, idInCol):
        ################################
        #The following must call base class's exists, as exists in this class 
        #is overrided
        if not collectionDatabase.collectionOnMongoDbBase.exists(self, idInCol):
            #The item is not in database, add it
            itemUuid = self.folderCollection.getObjUuid(idInCol)
            self.updateObjUuidRaw(idInCol, itemUuid)
            return itemUuid
        objUuid = collectionDatabase.collectionOnMongoDbBase.getObjUuid(self, idInCol)
        ncl("objUuid:", objUuid)
        if objUuid is None:
            #Does not exist
            return None
        else:
            return self.objDb.getFsObjFromUuid(objUuid)['uuid']


    #############################################
    # The following methods are called when this collection is dest
    # Called by archiver? only?
    #############################################
    def enumEnd(self, pendingCollection):
        pass
    def subClassEnumWithPending(self, timestamp, pendingCollection):
        for processingObjInCol, curTimestamp in self.enumWithPending(timestamp, pendingCollection):
            processingObjInfo = self.objDb.getObjFromUuid(processingObjInCol.getUuid())
            processingObj = syncFolderItem(self.rootDir, processingObjInfo)
            yield processingObj, curTimestamp
            
                
    def store(self, item, pendingCollection):
        #Check if the item in folder storage is newer than the target one
        relaPath = item["idInCol"]
        localFullPath = transform.transformDirToInternal(os.path.join(self.rootDir, relaPath))
        localPathDir = transform.transformDirToInternal(os.path.dirname(localFullPath))
        #Check the updates of the object is done in advCollectionProcess.
        #When we come here, the item is for sure needed for update
        
        #Backup if it exists
        if os.path.exists(localFullPath):
            backupFullPath = fileTools.getFreeNameFromFullPath(os.path.join(self.backupDir, relaPath))
            backupPathDir = os.path.dirname(backupFullPath)
            misc.ensureDir(backupPathDir)
            shutil.move(localFullPath, backupFullPath)
                
        misc.ensureDir(localPathDir)
        item.saveTo(self.rootDir)
        #################################
        #Update collection info
        #################################
        #Remove the legacy timestamp
        objInfo = copy.copy(item.getItemInfo())
        if objInfo.has_key("timestamp"):
            objInfo["externalTimestamp"] = objInfo["timestamp"]
            del objInfo["timestamp"]
        
        
        obj = objectDatabase.fsObjBase(localFullPath, objInfo)
        #ncl(obj.getItemInfo())
        #print type(obj.getItemInfo())
        #ncl(self.objDb.getDbObj(obj.getItemObjUrl()))
        itemUuid = self.objDb.addDbObj(obj.getObjUrl(), obj.getItemInfo())
        ncl("collection obj uuid:", itemUuid)
        #ncl(self.objDb.getDbObj(obj.getItemObjUrl()))
        self.updateObjUuid(item["idInCol"], itemUuid)
        return True