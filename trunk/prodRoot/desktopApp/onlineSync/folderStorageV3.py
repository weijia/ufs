import os
import localLibSys

import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import shutil
import localLibs.localTasks.infoCollector as infoCollector
import copy
from localLibs.logSys.logSys import *

class storageInterface:
    def getNextUpdatedItem(self, lastState):
        pass
    def store(self, item):
        pass
    def getState(self):
        return self.lastState.getState()
    def update(self, item):
        self.lastState.update(item)

'''
class folderStorageStateInterface:
    def updated(self, item):
        pass
    def updateModTime(self, item):
        pass
'''
class folderStorageState:
    def __init__(self, stateDict):
        self.stateDict = stateDict
        #print stateDict
    def updated(self, item):
        #print 'checking item for update: %s'%item.getItemId(), self.stateDict[item.getItemId()]
        try:
            #Item was recorded, check if timestamp changed
            if self.stateDict[item.getItemId()]["timestamp"] != item.getTimestamp():
                #File changed, check hash?
                if self.stateDict[item.getItemId()]["headMd5"] != item.getDataId():
                    #print 'time and hash does not match'
                    return True
                else:
                    #Timestamp is not equal but the content is equal, update the local timestamp
                    self.stateDict[item.getItemId()]["timestamp"] = item.getTimestamp()
                    print 'local file timestamp updated'
        except KeyError:
            return True
        #print 'getting info for:', item.getItemId()
        #print 'checking:--------------------'
        #print item.getItemInfo()
        #print self.stateDict[item.getItemId()]
        #print 'comparing time: %f, %f'%(self.stateDict[item.getItemId()]["timestamp"], item.getTimestamp())

        return False
            
    def update(self, item):
        self.stateDict[item.getItemId()] = item.getItemInfo()
    def getState(self):
        return self.stateDict
        
    def getItemState(self, item):
        try:
            return self.stateDict[item.getItemId()]
        except KeyError:
            return {}

            
class objBase:
    def __init__(self, fullPath, existingItemInfo = {}):
        self.fullPath = transform.transformDirToInternal(fullPath)
        self.itemInfo = copy.copy(existingItemInfo)

    #########################################################
    #The following methods are for dict
    #########################################################
    def itemAttr(self, key):
        if key == "fullPath":
            return self.fullPath
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
        return infoCollector.getHeadContentMd5(self.fullPath)
        
    def getItemInfo(self):
        tmp = self.fillInfo(["timestamp", "fullPath", "headMd5", "size"])
        return self.itemInfo
    def getItemObjUrl(self):
        return u"file:///"+self.fullPath
            
class storageItemBase(objBase):
    def __init__(self, rootPath, fullPath, existingItemInfo = {}):
        objBase.__init__(self, fullPath, existingItemInfo)
        self.rootPath = transform.transformDirToInternal(rootPath)

    
class storageItem(storageItemBase):        
    #########################################################
    #The following methods same for folder storage item and zip storage item
    #########################################################
    def getItemId(self):
        return self.getRelaPath()
    def getFullPath(self):
        return self.fullPath
    def getRelaPath(self):
        return transform.formatRelativePath(self.fullPath.replace(self.rootPath, ''))
        
    #########################################################
    #The following methods are must implemented
    #########################################################
    def getTimestamp(self):
        return self.itemAttr("timestamp")
    def getDataId(self):
        return self.itemAttr("headMd5")
    def getSize(self):
        return self.itemAttr("size")
    
        
        
class folderStorageItem(storageItem):
    def getExtTs(self):
        return self.itemInfo["externalItemTimestamp"]
    def isExternal(self):
        if self.itemInfo.has_key("externalItemTimestamp"):
            return True
        else:
            return False
        
class externalItem(folderStorageItem):
    def __init__(self, rootPath, fullPath, itemInfo):
        folderStorageItem.__init__(self, rootPath, fullPath)
        self.itemInfo = copy.copy(itemInfo)
        self.itemInfo["externalItemTimestamp"] = self.itemInfo["timestamp"]
        del self.itemInfo["timestamp"]

        
        
'''
def isItem1Newer(item1, item2):
    return item1.getTimestamp() > item2.getTimestamp()
'''
def isSameItems(item1, item2):
    if item1.getSize() != item2.getSize():
        #print 'not same size:', item1.getSize(), item2.getSize()
        return False
    if item1.getDataId() != item2.getDataId():
        #print 'not same data'
        return False
    return True
    
class folderStorage(storageInterface):
    def __init__(self, lastState, rootDir, backupDir):
        self.rootDir = rootDir
        self.backupDir = backupDir
        self.lastState = folderStorageState(lastState)
        
    def getNextUpdatedItem(self):
        for i in os.walk(self.rootDir):
            #print i
            for j in i[2]:
                fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
                #print fullPath
                item = folderStorageItem(self.rootDir, fullPath)
                if self.lastState.updated(item):
                    print '%s updated'%fullPath.encode('gbk','replace')
                    yield item
                self.lastState.update(item)
                
    def store(self, item):
        #Check if the item in folder storage is newer than the target one
        relaPath = item.getRelaPath()
        localFullPath = os.path.join(self.rootDir, relaPath)


        localItem = folderStorageItem(self.rootDir, localFullPath)
        extItem = externalItem(self.rootDir, localFullPath, item.getItemInfo())
        extItemLocalCopy = folderStorageItem(self.rootDir, localFullPath, self.lastState.getItemState(item))
        
        localPathDir = os.path.dirname(localFullPath)
        fullPath = item.getFullPath()
        if (not os.path.exists(localFullPath)):
            #Copy the updated file to local path
            misc.ensureDir(localPathDir)
            item.saveTo(self.rootDir)
            #Check if the timestamp are updated
            if localItem.getTimestamp() != extItem.timestamp():
                raise 'not work as expected, need to manually update time for local copy'
            self.lastState.update(extItem)
        elif self.lastState.updated(item):
            #print 'item updated:', item.getRelaPath()
            #The item has been updated, check content
            if isSameItems(item, localItem):
                print 'same, ignore:', fullPath.encode('gbk','replace'), localFullPath.encode('gbk','replace')
                #Need to update the item state
                self.lastState.update(extItem)
            else:
                #Seems external storage and local storage both updated this file. What to do? Ignore for now?
                pass
        else:
            #Not updated, check if the 2 items are same
            if isSameItems(item, extItemLocalCopy):
                print 'According to saved state, same, ignore:', fullPath.encode('gbk','replace'), localFullPath.encode('gbk','replace')
                #Need to update the item state
                self.lastState.update(extItem)
            elif extItemLocalCopy.isExternal():
                #It is an external file, check time
                if (extItemLocalCopy.getExtTs() < item.getTimestamp()):
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
                if extItemLocalCopy.getTimestamp < item.getTimestamp():
                    #External storage has updated the item, update the local one
                    backupFullPath = fileTools.getFreeNameFromFullPath(os.path.join(self.backupDir, relaPath))
                    backupPathDir = os.path.dirname(backupFullPath)
                    misc.ensureDir(backupPathDir)            
                    shutil.move(localFullPath, backupFullPath)
                    #Copy the updated file to local path
                    misc.ensureDir(localPathDir)
                    item.saveTo(self.rootDir)
                    self.lastState.update(extItem)
