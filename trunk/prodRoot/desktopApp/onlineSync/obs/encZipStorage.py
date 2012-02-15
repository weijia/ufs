import os
import localLibSys

import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
import localLibs.localTasks.infoCollector as infoCollector

import encZipWriteOnlyStorageV2 as encZipWriteOnlyStorage
import desktopApp.lib.compress.zipClass as zipClass
import folderStorage as folderStorage
import wwjufsdatabase.libs.utils.simplejson as json

'''
class zipStorageState:
    def __init__(self, stateDict):
        self.stateDict = stateDict
    def updated(self, item):
        try:
            if self.stateDict[item.getItemId()] == item.getTimestamp():
                return False
            return True
        except KeyError:
            return True
    def update(self, item):
        self.stateDict[item.getItemId()] = item.getTimestamp()
'''
    
def getTimeInSeconds(timeStructure):
    finalRes = []
    for i in timeStructure:
        finalRes.append(i)
    finalRes.extend([0,0,0])
    return time.mktime(finalRes)

class zipStorageItem:
    def __init__(self, relaPath, zipFileObj):
        self.relaPath = relaPath
        self.zipFileObj = zipFileObj
    '''
    #########################################################
    #The following methods are used only for tracking update state
    #########################################################
    def getTimestamp(self):
        return os.stat(self.fullPath).st_mtime
    def getItemId(self):
        return self.fullPath
    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    def getFullPath(self):
        return self.fullPath
    def getRelaPath(self):
        return self.fullPath.replace(self.rootPath+u'/', '')
    '''
class zipStorageItem(folderStorage.folderStorageItem):
    def __init__(self, rootPath, fullPath, infoDict):
        self.infoDict = infoDict
        self.rootPath = transform.transformDirToInternal(rootPath)
        self.fullPath = transform.transformDirToInternal(fullPath)
        folderStorage.folderStorageItem.__init__(self, rootPath, fullPath)

        
    #########################################################
    #The following methods are used only for tracking update state
    #########################################################
    def getTimestamp(self):
        if self.infoDict.has_key("timestamp"):
            return self.infoDict["timestamp"]
        return self.infoDict["zippedTimeStemp"]

    def getDataId(self):
        return self.infoDict["headMd5"]
    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    def getItemInfo(self):
        return self.infoDict

class encZipStorage(encZipWriteOnlyStorage.encZipWriteOnlyStorage):
    def __init__(self, lastState, workingDir, zipStorageDir, passwd):
        encZipWriteOnlyStorage.encZipWriteOnlyStorage.__init__(self, lastState, workingDir, zipStorageDir, passwd)
        self.zippedFileInfoRegenerating = {}
        self.regenerateNeeded = False
    
    def getNextUpdatedItem(self):
        #print 'zipdir:',self.zipStorageDir
        for walkingItem in os.walk(self.zipStorageDir):
            #print walkingItem
            for j in walkingItem[2]:
                encZipFileFullPath = transform.transformDirToInternal(os.path.join(walkingItem[0], j))
                print encZipFileFullPath
                zipFileFolderStorageItem = folderStorage.storageItem(self.zipStorageDir, encZipFileFullPath)
                if self.lastState.updated(zipFileFolderStorageItem):
                    ##################################################################
                    #For zip storage, if the zip file was updated (or newly created) we
                    #should enumerate all element in this zip file
                    ##################################################################
                    #First decrypt the zip file
                    if encZipFileFullPath.find('.enc') == -1:
                        #Not an encrypted zip file, continue
                        print 'not a encrypted zip file: ',encZipFileFullPath
                        continue
                    self.regenerateNeeded = False

                    zipFileFullPath = self.getZipFile(encZipFileFullPath)

                    #Enumerate all files in the decrypted zip file
                    zf = zipClass.ZFile(zipFileFullPath, 'r')
                    #Generate a log file if it does not exist
                    if not os.path.exists(encZipFileFullPath.replace('.enc','.enclog')):
                        self.regenerateNeeded = True
                        
                    for i in zf.list():
                        #yield zipStorageItem(i, zf)
                        zf.extract(i, self.workingDir)
                        extractedItemFullPath = os.path.join(self.workingDir, i)
                        extractedItemInfo = {"timestamp": getTimeInSeconds(zf.zfile.getinfo(i).date_time), 
                                    "headMd5":infoCollector.getHeadContentMd5(extractedItemFullPath), 
                                    "parentEncryptedZip":encZipFileFullPath, "size":os.stat(extractedItemFullPath).st_size, }
                                    
                        extractedItem = zipStorageItem(self.workingDir, 
                                os.path.join(self.workingDir, i))
                                
                        if self.regenerateNeeded:
                            relaPath = transform.formatRelativePath(i)
                            self.zippedFileInfoRegenerating[relaPath] = extractedItemInfo
                        yield extractedItem
                            
                    if self.regenerateNeeded:
                        self.saveRegeneratedState(encZipFileFullPath, zipFileFullPath)


