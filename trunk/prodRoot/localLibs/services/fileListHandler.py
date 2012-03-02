'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os

#from pprint import pprint

import localLibSys
from localLibs.storage.infoStorage.zippedCollectionWithInfo import zippedCollectionWithInfo
from localLibs.localFs.tmpFile import getStorgePathWithDateFolder
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
from fileListHandlerBase import fileListHandlerBase

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"

gMaxZippedCollectionSize = 0.5*1024

gZipCollectionRoot = "d:/tmp/generating"

class fileListHandler(fileListHandlerBase):
    '''
    classdocs
    '''
    def __init__(self, storage, zipCollectionRoot = gZipCollectionRoot, passwd = "123", fileListTubeName = gFileListTubeName):
        '''
        Constructor
        '''
        self.storage = storage
        self.zipCollectionRoot = zipCollectionRoot
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.curStorageSize = 0
        #self.addedList = []
        #self.fileListTubeName = fileListTubeName
        self.monitoringList = []
        super(fileListHandler, self).__init__(fileListTubeName)

    def processJob(self, job, item):
        if not (item['monitoringPath'] in self.monitoringList):
            self.monitoringList.append(item['monitoringPath'])
        info = self.storage.addItem(item["fullPath"])
        #print "zipped size", info.compress_size
        self.curStorageSize += info.compress_size

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
    
if __name__ == "__main__":
    print 'starting fileListHandler'
    workingDir = "d:/tmp/working"
    s = fileListHandler(zippedCollectionWithInfo(workingDir))
    s.startServer()