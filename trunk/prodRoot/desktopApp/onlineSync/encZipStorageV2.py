import os
import localLibSys

import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
import localLibs.localTasks.infoCollector as infoCollector

import encZipWriteOnlyStorageV2 as encZipWriteOnlyStorage
import desktopApp.lib.compress.zipClass as zipClass
import folderStorageV3 as folderStorage
import wwjufsdatabase.libs.utils.simplejson as json
    
def getTimeInSeconds(timeStructure):
    finalRes = []
    for i in timeStructure:
        finalRes.append(i)
    finalRes.extend([0,0,0])
    return time.mktime(finalRes)
    

class extractedZipStorageItem(folderStorage.folderStorageItem):
    def __init__(self, rootPath, fullPath, itemInfo, zipFileObj, pathInZipFile):
        folderStorage.folderStorageItem.__init__(self, rootPath, fullPath)
        self.itemInfo = itemInfo
        self.rootPath = transform.transformDirToInternal(rootPath)
        self.fullPath = transform.transformDirToInternal(fullPath)
        self.zipFileObj = zipFileObj
        self.pathInZipFile = pathInZipFile

        # zippedTime = self.itemInfo["timestamp"]
        # #Update timestamp to local time
        # self.itemInfo["timestamp"] = os.stat(self.fullPath).st_mtime
        # self.itemInfo["zippedTimestamp"] = zippedTime

    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    def getItemInfo(self):
        return self.itemInfo
    def saveTo(self, targetRootPath):
        print 'saving to:', os.path.join(targetRootPath.encode('gbk','replace'), self.pathInZipFile.encode('gbk','replace'))
        self.zipFileObj.extract(self.pathInZipFile, targetRootPath)

class encZipStorage(encZipWriteOnlyStorage.encZipWriteOnlyStorage):

    def getZipFile(self, encrtypedZipFileFullPath):
        zipFileFullPath = os.path.join(self.decryptionWorkingDir, 
                os.path.basename(encrtypedZipFileFullPath).replace('.enc', '.zip'))
        ########################################
        #TODO: Remove the check and alreays decrypt the file
        ########################################
        if not os.path.exists(zipFileFullPath):
            print 'copy from %s to %s'%(encrtypedZipFileFullPath.encode('gbk','replace'), zipFileFullPath.encode('gbk','replace'))
            self.decCopier.copy(encrtypedZipFileFullPath, zipFileFullPath)
        '''
        if True:
            self.decCopier.copy(encrtypedZipFileFullPath, zipFileFullPath)
        '''
        return zipFileFullPath

    def getNextUpdatedItem(self):
        #print 'zipdir:',self.zipStorageDir
        for walkingItem in os.walk(self.zipStorageDir):
            #print walkingItem
            for j in walkingItem[2]:
                encZipFileFullPath = transform.transformDirToInternal(os.path.join(walkingItem[0], j))
                print encZipFileFullPath.encode('gbk','replace')
                zipFileFolderStorageItem = folderStorage.folderStorageItem(self.zipStorageDir, encZipFileFullPath)
                if self.lastState.isZipFileUpdated(zipFileFolderStorageItem):
                    ##################################################################
                    #For zip storage, if the zip file was updated (or newly created) we
                    #should enumerate all element in this zip file
                    ##################################################################
                    #First decrypt the zip file
                    import re
                    if re.search('\.enc$', encZipFileFullPath) is None:
                        #Not an encrypted zip file, continue
                        print 'not a encrypted zip file: ',encZipFileFullPath.encode('gbk','replace')
                        continue

                    zipFileFullPath = self.getZipFile(encZipFileFullPath)

                    #Enumerate all files in the decrypted zip file
                    zf = zipClass.ZFile(zipFileFullPath, 'r')
                    #Generate a log file if it does not exist
                        
                    for i in zf.list():
                        #zf.extract(i, self.workingDir)
                        extractedItemFullPath = os.path.join(self.workingDir, i)
                        extractedItemInfo = self.getItemState(i)
                        '''
                        try:
                            extractedItem = extractedZipStorageItem(self.workingDir, 
                                    os.path.join(self.workingDir, i), extractedItemInfo)
                        except KeyError:
                            print self.workingDir, i, extractedItemInfo
                            raise KeyError
                        '''
                        extractedItem = extractedZipStorageItem(self.workingDir, 
                                extractedItemFullPath, extractedItemInfo, zf, i)
                        yield extractedItem
                    self.lastState.zipFileUpdate(zipFileFolderStorageItem)


