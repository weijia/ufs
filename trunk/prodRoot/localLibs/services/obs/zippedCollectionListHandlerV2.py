'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import threading
import beanstalkc


import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from beanstalkServiceBaseV2 import beanstalkServiceBase, beanstalkServiceApp
from localLibs.storage.infoStorage.zippedInfo import zippedInfo
import localLibs.archiver.encryptionStorageBase as encryptionStorageBase
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import localLibs.objSys.objectDatabaseV3 as objectDatabase

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
#gInputTubeName = "fileListTube"
#gOutputTubeName = "fileListDelayed"
gItemDelayTime = 5
gDefaultTtr = 3600*24
gZipFolderCollectionPrefix = "zippedColllectionWithInfo://"
gZippedCollectionListServiceCmdTubeName = 'zippedCollectionListServiceCmdTube'
gInfoFilePrefix = 'zippedCollFile'
gInfoFileDecryptedExt = ".zip"
gZippedInfoCollectionId = u"uuid://7e61b299-3004-4f0a-94da-47601106da7b"

class zippedCollectionListHandler(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, tubeName, workingDir = "d:/tmp/working/zippedCollectionListHandler", passwd = '123'):
        misc.ensureDir(workingDir)
        super(zippedCollectionListHandler, self).__init__(tubeName)
        threading.Thread.__init__(self)
        # Stores collection instance for given monitoring path, all zipped objects
        # in this monitoring path will be stored in this collection
        self.collectionInDbForMonitoringPath = {}
        self.dbInst = objectDatabase.objectDatabase()
        self.workingDir = workingDir
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.zippedInfoCollectionList = collectionDatabase.collectionOnMongoDbBase(gZippedInfoCollectionId, self.dbInst.getCollectionDb())
        
    def run(self):
        self.startServer()
            
    def processItem(self, job, item):
        monitoringFullPath = transform.transformDirToInternal(item['monitoringPath'])
        archiveId = gZipFolderCollectionPrefix + monitoringFullPath
        if not self.collectionInDbForMonitoringPath.has_key(monitoringFullPath):
            self.collectionInDbForMonitoringPath[monitoringFullPath] = collectionDatabase.collectionOnMongoDbBase(archiveId, self.dbInst.getCollectionDb())
            objUuid = self.dbInst.addVirtualObj({"monitoringPath": monitoringFullPath, "zippedInfoCollectionId": archiveId});
            idInCol = objUuid
            self.zippedInfoCollectionList.addObj(idInCol, objUuid)
        #Save the item in the archive collection: zippedInfoColllection://D:/tmp/
        fullPath = transform.transformDirToInternal(item["fullPath"])
        relativePath = transform.getRelativePathFromFull(fullPath, monitoringFullPath)
        if not os.path.exists(fullPath):
            job.delete()
            return False#No job release, job was deleted.
        #################################################################
        # Start process the 
        #################################################################
        if not self.collectionInDbForMonitoringPath[monitoringFullPath].exists(relativePath):
            #This item is not in the collection, so we need to extract info from this item
            newObj = self.dbInst.getFsObjFromFullPath(fullPath)
            self.collectionInDbForMonitoringPath[monitoringFullPath].addObj(relativePath, newObj["uuid"])
            zipFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.workingDir, gInfoFileDecryptedExt, gInfoFilePrefix))
            self.decCopier.copy(fullPath, zipFilePath)
            for i in zippedInfo(self.workingDir).enumItems(zipFilePath):
                print '--------------------------------------------------'
                print i
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
            for i in zippedInfo(self.workingDir).enumZippedFiles(zipFilePath):
                fp = open(i, 'r')
                print 'data file extracted:', i
        '''
        else:
            #This item is not in the collection, so we need to extract info from this item
            newObj = self.dbInst.getFsObjFromFullPath(fullPath)
            self.collectionInDbForMonitoringPath[monitoringFullPath].addObj(relativePath, newObj["uuid"])
            zipFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.workingDir, gInfoFileDecryptedExt, gInfoFilePrefix))
            self.decCopier.copy(fullPath, zipFilePath)
            for i in zippedInfo(self.workingDir).enumItems(zipFilePath):
                print '--------------------------------------------------'
                print i
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
            for i in zippedInfo(self.workingDir).enumZippedFiles(zipFilePath):
                fp = open(i, 'r')
                print 'data file extracted:', i
        '''
        return True#Release job
            
            
class zippedCollectionListService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gZippedCollectionListServiceCmdTubeName):
        super(zippedCollectionListService, self).__init__(tubeName)
        self.taskDict = {}
        
    def processItem(self, job, item):
        inputTubeName = item["inputTubeName"]
        if self.taskDict.has_key(inputTubeName):
            job.delete()
            return False
        t = zippedCollectionListHandler(inputTubeName)
        self.taskDict[inputTubeName] = t
        t.start()
        return True
                
            
            
            
            
if __name__ == "__main__":
    s = zippedCollectionListService()
    s.startServer()