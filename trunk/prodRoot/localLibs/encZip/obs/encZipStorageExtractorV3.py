import re
import uuid
import os
import localLibs.localTasks.processorBase as processorBase
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import desktopApp.lib.compress.zipClass as zipClass
import desktopApp.onlineSync.encZipStorageV2 as encZipStorage
import localLibs.collection.folderCollectionV2 as folderCollection
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.misc as misc

gAppUuid = '60c4d90a-fe04-4647-99bf-e2f464b9c299'

class encZipExtractor(processorBase.cacheCollectionProcessorBase):
    def __init__(self, taskId, appUuid, collectionId, workingDir, passwd, targetCollection):
        processorBase.cacheCollectionProcessorBase.__init__(self, taskId, appUuid, collectionId)
        #This dir stores zip files which were decrypted
        self.workingDir = workingDir
        self.decryptionWorkingDir = workingDir + '/decrypted'
        misc.ensureDir(self.decryptionWorkingDir)
        self.logCollectionId = self.appConfigObj["logCollectionId"]
        self.logCollection = collectionDatabase.collectionOnMongoDbBase(self.logCollectionId, self.db.getCollectionDb())
        self.targetCollection = targetCollection
        self.passwd = passwd
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
    def getLogCollectionId(self):
        return self.logCollectionId
    def subClassInitialCfg(self):
        '''
        Used by sub class to create config for itself.
        '''
        return {"logCollectionId":unicode(str(uuid.uuid4()))}

    def subClassProcessItem(self, processingObj):
        #Check if the log file and data file are both OK
        encZipFileFullPath = processingObj["fullPath"]
        if not (re.search('\.enclog$', encZipFileFullPath) is None):
            #An encrypted zip file, go on
            if os.path.exists(encZipFileFullPath.replace('.enclog', '.enc')):
                #Log and Data are both OK
                encryptedZipLogPath = encZipFileFullPath
                ncl(encryptedZipLogPath)
                zipLogPath = os.path.join(self.decryptionWorkingDir, 
                        os.path.basename(encryptedZipLogPath).replace('.enclog', '.log'))
                ncl(zipLogPath)
                self.decCopier.copy(encryptedZipLogPath, zipLogPath)
                try:
                    f = open(zipLogPath,'r')
                    newLog = json.load(f)
                    f.close()
                except IOError:
                    newLog = None
                if not (newLog is None):
                    #########################
                    #Log loaded, update collection
                    #########################
                    for i in newLog:
                        relaPath = transform.formatRelativePath(i)
                        ncl(newLog[i])
                        #################
                        #Get collection
                        #################
                        if self.logCollection.exists(relaPath):
                            itemUuid = self.logCollection.getObjUuid(relaPath)
                            ncl("returned uuid:", itemUuid)
                            item = self.db.getObjFromUuid(itemUuid)
                            #Conflict, check if update needed
                            ncl(newLog[i]["timestamp"])
                            ncl(item["timestamp"])
                            if newLog[i]["timestamp"] > item["timestamp"]:
                                #The new item is newer, replace the old one
                                ncl('updating duplicated item to 1st one:', newLog[i]["timestamp"], item["timestamp"])
                                objUuid = self.db.addVirtualObj(newLog[i])
                                self.logCollection.updateObjUuid(relaPath, objUuid)
                            else:
                                ncl("no update, ignore")
                        else:
                            #Add object to obj db
                            objUuid = self.db.addVirtualObj(newLog[i])
                            #Add obj to collection
                            self.logCollection.addObj(relaPath, objUuid)
                            ncl("added new item", relaPath, newLog[i])
                
                    #################################
                    #Process data
                    #################################
                    encZipFileFullPath = transform.transformDirToInternal(encZipFileFullPath)
                    ncl(encZipFileFullPath)
                    
                    zipFileFullPath = self.getZipFile(encZipFileFullPath.replace(".enclog", ".enc"))
                    #For all element in the zip file
                    #Enumerate all files in the decrypted zip file
                    zf = zipClass.ZFile(zipFileFullPath, 'r')
                    #Generate a log file if it does not exist
                        
                    for i in zf.list():
                        #zf.extract(i, self.workingDir)
                        extractedItemFullPath = os.path.join(self.workingDir, i)
                        relaPath = transform.formatRelativePath(i)
                        extractedItemInfo = self.getItemState(relaPath)

                        extractedItem = encZipStorage.extractedZipStorageItem(self.workingDir, 
                                extractedItemFullPath, extractedItemInfo, zf, relaPath)
                        ###########################
                        #Store the file
                        ###########################
                        self.targetCollection.store(extractedItem)
                    ##########################
                    #Everything goes OK
                    #Quit
                    ##########################
                    return
                else:
                    cl('Load log file failed',encZipFileFullPath)
            else:
                #Data file not exist, push it back
                ncl('Data file not exist, push it back: ',encZipFileFullPath)
        else:
            ncl('not a encrypted zip file: ',encZipFileFullPath)
            return
        ############
        #Item not processed, push it back
        ############
        processorBase.cacheCollectionProcessorBase.subClassProcessItem(self, processingObj)
        
        
    def getZipFile(self, encrtypedZipFileFullPath):
        zipFileFullPath = os.path.join(self.decryptionWorkingDir, 
                os.path.basename(encrtypedZipFileFullPath).replace('.enc', '.zip'))
        ########################################
        #TODO: Remove the check and alreays decrypt the file
        ########################################
        if not os.path.exists(zipFileFullPath):
            ncl('copy from %s to %s'%(encrtypedZipFileFullPath, zipFileFullPath))
            self.decCopier.copy(encrtypedZipFileFullPath, zipFileFullPath)
        '''
        if True:
            self.decCopier.copy(encrtypedZipFileFullPath, zipFileFullPath)
        '''
        return zipFileFullPath
        
    def getItemState(self, itemRelaPath):
        #parser output: u'zipEncStorage://'+self.appConfigObj["processedItemCollectionId"]+"?"+i, newLog[i])
        itemUuid = self.logCollection.getObjUuid(itemRelaPath)
        ncl("got item uuid:", itemUuid, itemRelaPath)
        item = self.db.getObjFromUuid(itemUuid)
        if item is None:
            cl('Can not get info for itme:',item)
            raise 'Can not get info for itme'
        return item

        
def main():
    import sys
    #print sys.argv[1]
    f = folderCollection.folderCollection("D:/tmp/fileman/target/data", "D:/tmp/fileman/target/backup", 'uuid://6efe7a94-3c5d-47e6-97c2-1bfb84d2bd24')
    s = encZipExtractor("test task2", gAppUuid, "D:/tmp/fileman/data", "D:/tmp/dbOrientTest", sys.argv[1], f)
    s.process()
    
     
if __name__ == '__main__':
    main()
