'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os
import threading

#from pprint import pprint

import localLibSys
from localLibs.storage.infoStorage.zippedCollectionWithInfo import zippedCollectionWithInfo
from localLibs.storage.infoStorage.zippedInfoWithThumb import zippedInfoWithThumb
from localLibs.localFs.tmpFile import getStorgePathWithDateFolder
import localLibs.archiver.encryptionStorageBase as encryptionStorageBase
from beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp
import localLibs.objSys.objectDatabaseV3 as objectDatabase
import wwjufsdatabase.libs.utils.misc as misc

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"

gMaxZippedCollectionSize = 0.005*1024

gZipCollectionRoot = "d:/tmp/generating"


class fileArchiveThread(beanstalkWorkingThread):
    def __init__ ( self, inputTubeName, storage, zipCollectionRoot = gZipCollectionRoot, passwd = "123"):
        '''
        Constructor
        '''
        super(fileArchiveThread, self).__init__(inputTubeName)
        self.storage = storage
        self.zipCollectionRoot = zipCollectionRoot
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.curStorageSize = 0
        #self.addedList = []
        #self.fileListTubeName = fileListTubeName
        self.monitoringList = []
        self.dbInst = objectDatabase.objectDatabase()

    def processItem(self, job, item):
        if not (item['monitoringPath'] in self.monitoringList):
            self.monitoringList.append(item['monitoringPath'])
        itemObj = self.dbInst.getFsObjFromFullPath(item["fullPath"])
        #print itemObj["uuid"]
        addedItemSize = self.storage.addItem(itemObj)   
        #print "zipped size", info.compress_size
        self.curStorageSize += addedItemSize
        #print "current size:", self.curStorageSize
        if self.curStorageSize > gMaxZippedCollectionSize:
            self.storage.addAdditionalInfo({"monitoringPathList": self.monitoringList})
            zipFullPath = self.storage.finalizeZipFile()
            targetPath = getStorgePathWithDateFolder(self.zipCollectionRoot)
            self.encCopier.copy(zipFullPath, targetPath)
            self.monitoringList = []
            #print 'old file zipped, new file created'
            #TODO: Remove tmp file.
            
            #All jobs processed completely, return True
            return True
        #Return False as jobs are not processed completely
        return True
    

        
class fileArchiveService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, storageClass = zippedInfoWithThumb, serviceControlTubeName = "fileArchiveServiceTubeName"):
        super(fileArchiveService, self).__init__(serviceControlTubeName)
        self.taskDict = {}
        self.storageClass = storageClass

        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        workingDir = item["workingDir"]
        misc.ensureDir(workingDir)
        inputTubeName = item["inputTubeName"]
        if self.taskDict.has_key(inputTubeName):
            job.delete()
            return False
        t = fileArchiveThread(inputTubeName, self.storageClass(workingDir))
        self.taskDict[inputTubeName] = t
        t.start()
        return True
                

if __name__ == "__main__":
    print 'starting fileListHandler'
    workingDir = "d:/tmp/working"
    s = fileArchiveService()
    s.startServer()