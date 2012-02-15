import encZipStorageCollectionEnum as encZipStorageCollectionEnum
import wwjufsdatabase.libs.utils.transform as transform
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.simplejson as json
import desktopApp.lib.compress.zipClass as zipClass
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import os

MAX_SINGLE_ARCHIVE_SIZE = 10*1024*1024


class encZipCollection(encZipStorageCollectionEnum.encZipStorageCollectionEnum):
    def __init__(self, collectionId, logCollectionId, workingDir, passwd, dbInst):
        '''
        collectionId is the ID of the enc zip storage collection, it should be the dir path storing 
        the enc zip files, and it will be used to retieve all enc zip files.
        '''
        encZipStorageCollectionEnum.encZipStorageCollectionEnum.__init__(self, collectionId, logCollectionId, workingDir, passwd, dbInst)
        
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
        
        self.zipStorageDir = transform.transformDirToInternal(collectionId)
        misc.ensureDir(self.zipStorageDir)

    def store(self, processingObj, pendingCollection):
        '''
        processingObj = {"fullPath": "D:/tmp/good.txt", "size":100}
        '''
        ncl(processingObj)
        #relaPath = transform.formatRelativePath(item.getRelaPath())
        relaPath = processingObj.getIdInCol()
        ncl('Got relaPath')
        if (pendingCollection.has_key(relaPath)) and (pendingCollection[relaPath] != processingObj["uuid"]):
            pendingCollection[relaPath] = processingObj["uuid"]
            ncl('Added to pending')
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
            self.encZip(pendingCollection)
            self.createNewZip()
        ncl('after encryption')

        ##############################
        #Add the file to zip file
        ##############################
        #print 'copying "%s" to "%s"'%(fullPath, relPath)
        self.curArchive.addfile(unicode(fullPath), unicode(relaPath))
        self.curArchivedSize += os.stat(fullPath).st_size

        processingObj["parentEncZip"] = self.targetPath.replace(".zip", ".enc")
        self.zippedFileInfo[relaPath] = processingObj.getItemInfo()
        ncl('return from store')
            
        
    ################################################
    # The following methods are only used internally
    ################################################
    def createNewZip(self):
        ####################
        # Create new zip file
        ####################
        gTimeV = time.gmtime()
        yearStr = time.strftime("%Y", gTimeV)
        monthStr = time.strftime("%m", gTimeV)
        dayStr = time.strftime("%d", gTimeV)
        dateTimeDir = yearStr+"/"+monthStr+"/"+dayStr
        newEncDir = unicode(os.path.join(self.zipStorageDir, dateTimeDir))
        misc.ensureDir(newEncDir)
        self.curArchiveName = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.workingDir, '.zip'))
        self.targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(newEncDir, '.enc'))
        cl("Creating new zip file", self.curArchiveName)
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

        cl('copying "%s" to "%s"'%(self.curArchiveName, self.targetPath))

        ##############################
        ############################################
        #TODO: update the processed item list, so this new created item will not be processed by the extractor again
        self.encCopier.copy(self.curArchiveName, self.targetPath)
        
        ############################
        # Save info for zipped files
        ############################
        s = json.dumps(self.zippedFileInfo, sort_keys=True, indent=4)
        logFilePath = self.curArchiveName.replace(u'.zip', u'.log')
        f = open(logFilePath,'w')
        f.write(s)
        f.close()
        logZipPath = self.curArchiveName.replace(u'.zip',u'.log.zip')
        logZip = zipClass.ZFile(logZipPath, 'w')
        logZip.addfile(unicode(logFilePath), os.path.basename(logFilePath))
        logZip.close()
        ############################################
        #TODO: update the processed item list, so this new created item will not be processed by the extractor again
        self.encCopier.copy(logZipPath, self.targetPath.replace('.enc', '.encziplog'))
        
        
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
            self.logCollection.updateObjUuid(relaPath, newLog[i]["uuid"])

    def enumEnd(self, pendingCollection):
        self.encZip(pendingCollection)
