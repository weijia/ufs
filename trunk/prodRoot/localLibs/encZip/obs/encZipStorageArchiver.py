import localLibs.localTasks.processorBase as processorBase
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import desktopApp.onlineSync.folderStorageV3 as folderStorage
import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
from localLibs.logSys.logSys import *


MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024


class encZipArchiver(processorBase.cacheCollectionProcessorBase):
    def __init__(self, taskId, appUuid, rootDir, workingDir, passwd, encZipStorageCollectionId, folderStorageCollectionId):
        self.rootDir = transform.transformDirToInternal(rootDir)
        processorBase.cacheCollectionProcessorBase.__init__(self, taskId, appUuid, self.rootDir)
        ########################################
        #Internal used vars
        ########################################
        #The current zipfile object
        self.curArchive = None
        #Not necessary init as it will be inited with self.curArchive
        #The current archived size
        self.curArchivedSize = 0
        self.logCollectionId = encZipStorageCollectionId
        self.logCollection = collectionDatabase.collectionOnMongoDbBase(self.logCollectionId, self.db.getCollectionDb())
        self.folderStorageCollectionId = folderStorageCollectionId
        self.folderStorageCollection = collectionDatabase.collectionOnMongoDbBase(self.folderStorageCollectionId, self.db.getCollectionDb())
        
        #The info of files in the current zip file
        self.zippedFileInfo = {}
        
        #The info of the whole storage
        self.zipStorageState = None
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.workingDir = workingDir

    def afterProcess(self, curItem):
        '''
        Overide the function so the time stamp was updated by this sub class
        '''
        #Update cursor in database to indicate that the encZip file was processed
        #self.db.updateObjByUuid(self.appConfigObj["uuid"], {"nextToProcessTimestamp": curItem["timestamp"]})
        pass

    def subClassProcessItem(self, processingObj):
        '''
        processingObj = {"fullPath": "D:/tmp/good.txt", "size":100}
        '''
        ncl(processingObj)
        fullPath = transform.transformDirToInternal(processingObj["fullPath"])
        relaPath = transform.formatRelativePath(fullPath.replace(self.rootDir, ''))
        if self.logCollection.exists(relaPath):
            #Item exists, check if it is updated
            collectionItem = self.db.getObjFromUuid(self.logCollection.getObjUuid(relaPath))
            if collectionItem["timestamp"] > processingObj["timestamp"]:
                #Want to update an older file to a newer file. Ignore it
                pass
            elif (collectionItem["timestamp"] == processingObj["timestamp"]) or (collectionItem["headMd5"] == processingObj["headMd5"]):
                #The 2 item is the same, ignore it
                pass
            else:
                if self.curArchive is None:
                    self.createNewZip()

                if (self.curArchivedSize > MAX_SINGLE_ARCHIVE_SIZE):
                    self.encZip()
                    self.createNewZip()
                    
                #Add the file to zip
                try:
                    #If there is already an item with the same name, ignore the current?
                    existingElem = self.zipContentState[transform.formatRelativePath(i)]
                    return
                except:
                    pass

                ##############################
                #Add the file to zip file
                ##############################
                #print 'copying "%s" to "%s"'%(fullPath, relPath)
                self.curArchive.addfile(unicode(fullPath).encode('gbk'), unicode(relaPath).encode('gbk'))
                self.curArchivedSize += os.stat(fullPath).st_size
                '''
                itemInfo = item.getItemInfo()
                itemInfo["parentEncZip"] = self.curArchiveName.replace(".zip", ".enc")
                self.zippedFileInfo[relaPath] = itemInfo
                '''
                processingObj["parentEncZip"] = self.curArchiveName.replace(".zip", ".enc")
                self.zippedFileInfo[relaPath] = processingObj
                
            
        
    ################################################
    # The following methods are only used internally
    ################################################
    def createNewZip(self):
        ####################
        # Create new zip file
        ####################
        cl("Creating new zip file")
        self.curArchiveName = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.workingDir, '.zip'))
        self.curArchive = zipClass.ZFile(self.curArchiveName, 'w')
        self.curArchivedSize = 0
        
    def encZip(self):
        #Must close the zip before encrypt it, otherwise, the file are not integrate
        if self.curArchive is None:
            return
        self.curArchive.close()
        self.curArchive = None
        
        ############################
        # Encrypt the zip file
        ############################
        targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.zipStorageDir, '.enc'))
        print 'copying "%s" to "%s"'%(self.curArchiveName, targetPath)

        ##############################
        ############################################
        #TODO: update the processed item list, so this new created item will not be processed by the extractor again
        self.encCopier.copy(self.curArchiveName, targetPath)
        
        ############################
        # Save info for zipped files
        ############################
        s = json.dumps(self.zippedFileInfo, sort_keys=True, indent=4)
        f = open(self.curArchiveName.replace('.zip', '.log'),'w')
        f.write(s)
        f.close()
        ############################################
        #TODO: update the processed item list, so this new created item will not be processed by the extractor again
        self.encCopier.copy(self.curArchiveName.replace('.zip', '.log'), targetPath.replace('.enc', '.enclog'))
        
        
        ############################
        # Update state in storage state
        ############################
        self.updateZipLog(self.zippedFileInfo)
        #Clean the current zipped file info
        self.zippedFileInfo = {}


        
    def updateZipLog(self, newLog):
        for i in newLog:
            relaPath = transform.formatRelativePath(i)
            if self.logCollection.exists(relaPath):
                objUuid = self.db.addVirtualObj(newLog[i])
                self.logCollection.updateObjUuid(relaPath, objUuid)
            else:
                #Add object to obj db
                objUuid = self.db.addVirtualObj(newLog[i])
                #Add obj to collection
                self.logCollection.addObj(relaPath, objUuid)

