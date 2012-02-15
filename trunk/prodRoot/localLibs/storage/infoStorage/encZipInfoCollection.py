import encZipInfoCollectionEnum as encZipInfoCollectionEnum
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.simplejson as json
import desktopApp.lib.compress.zipClass as zipClass
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import os

MAX_FILE_CNT_IN_INFO_FILE = 10000


class encZipInfoCollection(encZipInfoCollectionEnum.encZipInfoCollectionEnum):
    def __init__(self, collectionId, logCollectionId, workingDir, passwd, dbInst):
        '''
        collectionId is the ID of the enc zip storage collection, it should be the dir path storing 
        the enc zip files, and it will be used to retieve all enc zip files.
        '''
        super(encZipInfoCollection, self).__init__(collectionId, logCollectionId, workingDir, passwd, dbInst)
        
        ########################################
        #Internal used vars
        ########################################
        #The info of files in the current zip file
        self.zippedFileInfo = {}
        
        #File count for the current info storage, encZipCollection does
        #not have this
        self.fileCnt = 0
        
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
            #Item exists in pending but uuid is not the same, update the uuid for the pending item
            pendingCollection[relaPath] = processingObj["uuid"]
            cl('Added to pending')
        fullPath = transform.transformDirToInternal(processingObj["fullPath"])

        #Add the file to zip
        try:
            #If there is already an item with the same name, ignore the current?
            existingElem = self.zippedFileInfo[relaPath]
            return
        except:
            pass


        if (self.fileCnt > MAX_FILE_CNT_IN_INFO_FILE):
            self.encInfoZip(pendingCollection)

        processingObj["parentEncZip"] = self.targetPath.replace(".zip", ".enc")
        self.zippedFileInfo[relaPath] = processingObj.getItemInfo()
        cl('return from store')
            
        
    def encInfoZip(self, pendingCollection):
        ############################
        # Save info for zipped files
        ############################
        logFilePath = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.workingDir, '.log'))
        s = json.dumps(self.zippedFileInfo, sort_keys=True, indent=4)
        f = open(logFilePath,'w')
        f.write(s)
        f.close()
        logZipPath = logFilePath.replace(u'.log',u'.log.zip')
        logZip = zipClass.ZFile(logZipPath, 'w')
        logZip.addfile(unicode(logFilePath), os.path.basename(logFilePath))
        logZip.close()
        
        gTimeV = time.gmtime()
        yearStr = time.strftime("%Y", gTimeV)
        monthStr = time.strftime("%m", gTimeV)
        dayStr = time.strftime("%d", gTimeV)
        dateTimeDir = yearStr+"/"+monthStr+"/"+dayStr
        newEncDir = unicode(os.path.join(self.zipStorageDir, dateTimeDir))
        misc.ensureDir(newEncDir)
        targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(newEncDir, '.enc'))
        self.encCopier.copy(logZipPath, targetPath.replace('.enc', '.encziplog'))
        
        
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
        self.encInfoZip(pendingCollection)
