'''
Created on 2011-9-28

@author: Richard
'''


import re
import uuid
import os
#import localLibs.localTasks.processorBase as processorBase
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import localLibs.collection.objectDatabaseV2 as objectDatabase
import desktopApp.lib.compress.zipClass as zipClass
import localLibs.collection.synchronizableCollection as synchronizableCollection
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.misc as misc
import copy
import localLibs.collection.folderRecursiveEnumCollection as folderRecursiveEnumCollection

gAppUuid = '587da5a2-7a3a-4ce1-90c3-5533e3462819'

gTargetEncLog = '.encziplog'
gTargetEncLogPattern = '\.encziplog'
gTargetEnc = '.enc'
gZipLogExt = '.log.zip'
gLogExt = '.log'


class collectionLog(synchronizableCollection.synchronizableCollection):
    def __init__(self, collectionId, logCollectionId, workingDir, passwd, dbInst):
        '''
        collectionId is the id of a collection contains all enc zip files
        logCollectionId is the id of a collection contains all extracted info
        '''
        self.objDb = dbInst
        self.collectionDbInst = dbInst.getCollectionDb()
        #This dir stores zip files which were decrypted
        self.workingDir = workingDir
        self.decryptionWorkingDir = workingDir + '/decrypted'
        misc.ensureDir(self.decryptionWorkingDir)
        #This is the folder collection that contains all encrypted zip files
        self.collectionId = collectionId
        ncl(collectionId)
        self.collection = folderRecursiveEnumCollection.folderRecursiveEnumCollection(self.collectionId, dbInst)
        
        #This is the log collection which stores all extracted info, these info may 
        #be extracted every time the folder is scaned, but it'll be better to store them for future use
        self.logCollectionId = logCollectionId
        self.logCollection = collectionDatabase.collectionOnMongoDbBase(self.logCollectionId, self.collectionDbInst)
        
        self.passwd = passwd
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)

    #############################################
    # The following methods are for synchronizable collection
    #############################################
    def exists(self, idInCol):
        '''
        Check if the item is in the enc zip collection. It means that check if
        the item is in the folder which inlucdes the encrypted zip files
        '''
        return self.logCollection.exists(idInCol)
    
    def enumObjs(self, timestamp):
        return self.collection.enumObjs(timestamp)
    
    #############################################
    # The following methods are for collection and synchronizer
    #############################################
    def getObjUuid(self, idInCol):
        return self.logCollection.getObjUuid(idInCol)
        


    def subClassEnumWithPending(self, timestamp, pendingCollection):
        for processingObjInCol, curTimestamp in self.enumWithPending(timestamp, pendingCollection):
            processingObj = self.objDb.getObjFromUuid(processingObjInCol.getUuid())
            encZipFileFullPath = processingObj["fullPath"]
            cl(encZipFileFullPath)
            if not (re.search(gTargetEncLogPattern, encZipFileFullPath) is None):
                #An encrypted zip file, go on
                if os.path.exists(encZipFileFullPath.replace(gTargetEncLog, gTargetEnc)):
                    #Log and Data are both OK, generate items
                    for curObj in self.subClassProcessItem(processingObj):
                        ##########################
                        # Returning object and timestamp
                        ##########################
                        yield curObj, curTimestamp
                else:
                    #Data file not exist, push it back
                    pendingCollection.updateObjUuid(processingObjInCol.getIdInCol(), processingObjInCol.getUuid())
                    cl('Data file not exist',encZipFileFullPath,
                       encZipFileFullPath.replace(gTargetEncLog, gTargetEnc))
            else:
                cl('not a encrypted zip file: ',encZipFileFullPath)
                
                

    #############################################
    # The following methods are for internal use
    #############################################
    def subClassProcessItem(self, processingObj):
        encZipFileFullPath = processingObj["fullPath"]
        encryptedZipLogPath = encZipFileFullPath
        ncl(encryptedZipLogPath)
        zipLogPath = os.path.join(self.decryptionWorkingDir, 
                os.path.basename(encryptedZipLogPath).replace(gTargetEncLog, gZipLogExt))
        cl(zipLogPath)
        self.decCopier.copy(encryptedZipLogPath, zipLogPath)
        
        #Extract log file from zip
        logZip = zipClass.ZFile(zipLogPath, 'r')
        #logPath = zipLogPath.replace(gZipLogExt, gLogExt)
        logLoaded = False
        for logFileName in logZip.list():
            logZip.extract(logFileName, self.decryptionWorkingDir)
            logPath = os.path.join(self.decryptionWorkingDir, logFileName)
            #cl(logPath)
            #Read log file
            try:
                f = open(logPath,'r')
                newLog = json.load(f)
                f.close()
            except IOError:
                newLog = None
                raise 'log not read'
            if not (newLog is None):
                #########################
                #Log loaded, update collection
                #########################
                logLoaded = True
                print 'extracting info from log', encZipFileFullPath
                for i in newLog:
                    relaPath = transform.formatRelativePath(i)
                    ncl(newLog[i])
                    #Remove the uuid in log file
                    if newLog[i].has_key("uuid"):
                        newLog[i]["originalUuid"] = newLog[i]["uuid"]
                        del newLog[i]["uuid"]
                    #################
                    #Get collection
                    #################
                    if self.logCollection.exists(relaPath):
                        itemUuid = self.logCollection.getObjUuid(relaPath)
                        ncl("returned uuid:", itemUuid)
                        item = self.objDb.getObjFromUuid(itemUuid)
                        #Conflict, check if update needed
                        ncl(newLog[i]["timestamp"])
                        ncl(item["timestamp"])
                        if newLog[i]["timestamp"] > item["timestamp"]:
                            #The new item is newer, replace the old one
                            ncl('updating duplicated item to 1st one:', newLog[i]["timestamp"], item["timestamp"])
                            objUuid = self.objDb.addVirtualObj(newLog[i])
                            self.logCollection.updateObjUuid(relaPath, objUuid)
                        else:
                            ncl("no update, ignore")
                    else:
                        #Add object to obj objDb
                        objUuid = self.objDb.addVirtualObj(newLog[i])
                        #Add obj to collection
                        self.logCollection.addObj(relaPath, objUuid)
                        ncl("added new item", relaPath, newLog[i])
        if logLoaded:
            #################################
            #Process data
            #################################
            print 'extracting info from log complete', encZipFileFullPath
            encZipFileFullPath = transform.transformDirToInternal(encZipFileFullPath)
            ncl(encZipFileFullPath)
            
            zipFileFullPath = self.getZipFile(encZipFileFullPath.replace(gTargetEncLog, gTargetEnc))
            #For all element in the zip file
            #Enumerate all files in the decrypted zip file
            zf = zipClass.ZFile(zipFileFullPath, 'r')
            #Generate a log file if it does not exist
                
            for i in zf.list():
                #zf.extract(i, self.workingDir)
                extractedItemFullPath = os.path.join(self.workingDir, i)
                relaPath = transform.formatRelativePath(i)
                ncl(relaPath)
                extractedItemInfo = self.getItemState(relaPath)

                extractedItem = extractedZipStorageItem(self.workingDir,
                        extractedItemFullPath, extractedItemInfo, zipFileFullPath, zf, relaPath)
                '''
                ###########################
                #Store the file
                ###########################
                #self.targetCollection.store(extractedItem)
                '''
                ###########################
                # Returning object
                ###########################
                yield extractedItem
            ##########################
            #Everything goes OK
            #Quit
            ##########################
            return
        else:
            cl('Load log file failed',encZipFileFullPath)

        
        
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
        item = self.objDb.getObjFromUuid(itemUuid)
        #item["originalUuid"] = item["uuid"]
        #del item["uuid"]
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
