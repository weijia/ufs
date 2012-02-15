import os
import localLibSys

import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import shutil
import localLibs.localTasks.infoCollector as infoCollector

class storageInterface:
    def getNextUpdatedItem(self, lastState):
        pass
    def store(self, item):
        pass
    def getState(self):
        return self.lastState.getState()
    def update(self, item):
        self.lastState.update(item)
        
class folderStorageStateInterface:
    def updated(self, item):
        pass
    def updateModTime(self, item):
        pass
        
class folderStorageState:
    def __init__(self, stateDict):
        self.stateDict = stateDict
    def updated(self, item):
        #print 'checking item for update: %s'%item.getItemId(), self.stateDict[item.getItemId()]
        try:
            #Item was recorded, check if timestamp changed
            if self.stateDict[item.getItemId()]["timestamp"] != item.getTimestamp():
                #File changed, check hash?
                if self.stateDict[item.getItemId()]["headMd5"] != infoCollector.getHeadContentMd5(
                                        item.getFullPath()):
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
        # print self.stateDict[item.getItemId()]
        # print 'comparing time: %f, %f'%(self.stateDict[item.getItemId()]["timestamp"], item.getTimestamp())

        return False
            
    def update(self, item):
        self.stateDict[item.getItemId()] = item.getItemInfo()
    def getState(self):
        return self.stateDict
        
    def getItemState(self, item):
        return self.stateDict[item.getItemId()]

        
class storageItem:
    def __init__(self, rootPath, fullPath):
        self.rootPath = transform.transformDirToInternal(rootPath)
        self.fullPath = transform.transformDirToInternal(fullPath)
        
    #########################################################
    #The following methods are used only for tracking update state
    #########################################################
    def getTimestamp(self):
        return os.stat(self.fullPath).st_mtime
    def getItemId(self):
        return self.getRelaPath()

    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    def getFullPath(self):
        return self.fullPath
    def getRelaPath(self):
        return transform.formatRelativePath(self.fullPath.replace(self.rootPath, ''))

class folderStorageItem(storageItem):
    def __init__(self, rootPath, fullPath):#, storageState):
        storageItem.__init__(self, rootPath, fullPath)
        #self.storageState = storageState
        
    #########################################################
    #The following methods are used only for tracking update state
    #########################################################
    '''
    def getTimestamp(self):
        return os.stat(self.fullPath).st_mtime
    def getItemId(self):
        return self.getRelaPath()
    '''
    def getItemInfo(self):
        return {"timestamp": self.getTimestamp(), "fullPath":self.getFullPath(),
                "headMd5":infoCollector.getHeadContentMd5(self.getFullPath()), "size":os.stat(self.getFullPath()).st_size}
    '''
    def getDataId(self):
        try:
            return self.storageState.getItemState()["headMd5"]
        except KeyError:
            return infoCollector.getHeadContentMd5(self.getFullPath())
    '''
    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    '''
    def getFullPath(self):
        return self.fullPath
    def getRelaPath(self):
        return transform.formatRelativePath(self.fullPath.replace(self.rootPath, ''))
    '''
    
def isItem1Newer(item1, itme2):
    item1FullPath = item1.getFullPath()
    item2FullPath = item2.getFullPath()
    
    return (os.stat(item1FullPath).st_mtime > os.stat(item2FullPath).st_mtime)
        
def isSameItems(item1, item2):
    item1FullPath = item1.getFullPath()
    item2FullPath = item2.getFullPath()
    if os.stat(item1FullPath).st_size != os.stat(item2FullPath).st_size:
        return False
    if infoCollector.getHeadContentMd5(item1FullPath) != infoCollector.getHeadContentMd5(item2FullPath):
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
                    #print '%s updated'%fullPath
                    yield item
                self.lastState.update(item)
                
    def store(self, item):
        #Check if the item in folder storage is newer than the target one
        fullPath = item.getFullPath()
        relaPath = item.getRelaPath()
        localFullPath = os.path.join(self.rootDir, relaPath)
        localItem = folderStorageItem(self.rootDir, localFullPath)
        localPathDir = os.path.dirname(localFullPath)
        if (not os.path.exists(localFullPath)):
            #Copy the updated file to local path
            misc.ensureDir(localPathDir)
            shutil.move(fullPath, localFullPath)
            #print localFullPath
            self.lastState.update(item)
        elif isSameItems(item, localItem):
            print 'same, ignore:', fullPath, localFullPath
        elif isItem1Newer(item, localItem):
            #The file need to be stored is newer, copy the older file to backup storage
            backupFullPath = fileTools.getFreeNameFromFullPath(os.path.join(self.backupDir, relaPath))
            backupPathDir = os.path.dirname(backupFullPath)
            misc.ensureDir(backupPathDir)            
            shutil.move(localFullPath, backupFullPath)
            #Copy the updated file to local path
            misc.ensureDir(localPathDir)
            shutil.copy(fullPath, localFullPath)
            self.lastState.update(item)
        else:
            #The file need to be stored is old, copy it to backup storage
            backupFullPath = fileTools.getFreeNameFromFullPath(os.path.join(self.backupDir, relaPath))
            backupPathDir = os.path.dirname(backupFullPath)
            misc.ensureDir(backupPathDir)            
            shutil.copy(fullPath, backupPathDir)

