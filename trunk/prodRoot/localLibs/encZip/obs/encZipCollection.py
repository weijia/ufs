import localLibs.localTasks.processorBase as processorBase
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
#import desktopApp.onlineSync.folderStorageV3 as folderStorage
import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.fileTools as fileTools


MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024


class encZipCollection(collectionDatabase.collectionOnMongoDbBase):
    def __init__(self, rootDir, workingDir, passwd, collectionId, mongoDbInst):
        collectionDatabase.collectionOnMongoDbBase.__init__(self, collectionId, mongoDbInst):
        self.rootDir = transform.transformDirToInternal(rootDir)
        
        ########################################
        #Internal used vars
        ########################################
        #The current zipfile object
        self.curArchive = None
        
        #Not necessary init as it will be inited with self.curArchive
        #The current archived size
        self.curArchivedSize = 0
        
        #The info of files in the current zip file
        self.zippedFileInfo = {}
        
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.workingDir = workingDir


    def store(self, processingObj, pendingCollection):
        '''
        processingObj = {"fullPath": "D:/tmp/good.txt", "size":100}
        '''
        ncl(processingObj)
        #relaPath = transform.formatRelativePath(item.getRelaPath())
        relaPath = transform.formatRelativePath(fullPath.replace(self.rootDir, ''))
        pendingCollection[relaPath] = processingObj["uuid"]
        fullPath = transform.transformDirToInternal(processingObj["fullPath"])

        #Add the file to zip
        try:
            #If there is already an item with the same name, ignore the current?
            existingElem = self.zippedFileInfo[relaPath]
            return
        except:
            pass


        if self.curArchive is None:
            self.createNewZip()

        if (self.curArchivedSize > MAX_SINGLE_ARCHIVE_SIZE):
            self.encZip()
            self.createNewZip()
            

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
        
    def encZip(self, pendingCollection):
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
        cl('copying "%s" to "%s"'%(self.curArchiveName, targetPath))

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
        self.updateZipLog(self.zippedFileInfo, pendingCollection)
        #Clean the current zipped file info
        self.zippedFileInfo = {}


        
    def updateZipLog(self, newLog, pendingCollection):
        for i in newLog:
            relaPath = transform.formatRelativePath(i)
            del pendingCollection[relaPath]
            self.updateObjUuid(relaPath, i["uuid"])


