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
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
from localLibs.objSys.objectDatabaseV3 import objectDatabase
from localLibs.storage.infoStorage.zippedInfo import zippedInfo
import wwjufsdatabase.libs.utils.simplejson as json

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"

gMaxZippedCollectionSize = 0.5*1024

gZipCollectionRoot = "d:/tmp/generating"
gWorkingDir = "d:/tmp/working"

class zippedCollectionListHandler(fileListHandlerBase):
    '''
    classdocs
    '''
    def __init__(self, fileListTubeName = gFileListTubeName, passwd = "123", workingDir = gWorkingDir):
        '''
        Constructor
        '''
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.collectionInDbForMonitoringPath = {}
        self.workingDir = workingDir
        self.dbInst = objectDatabase()
        super(zippedCollectionListHandler, self).__init__(fileListTubeName)

    def processJob(self, job, item):
        monitoringFullPath = transform.transformDirToInternal(item['monitoringPath'])
        archiveId = "zippedInfoColllection://" + monitoringFullPath
        if not self.collectionInDbForMonitoringPath.has_key(monitoringFullPath):
            self.collectionInDbForMonitoringPath[monitoringFullPath] = collectionDatabase.collectionOnMongoDbBase(archiveId, self.dbInst.getCollectionDb())
        #Save the item in the archive collection: zippedInfoColllection://D:/tmp/
        fullPath = transform.transformDirToInternal(item["fullPath"])
        relativePath = transform.getRelativePathFromFull(fullPath, monitoringFullPath)
        if not self.collectionInDbForMonitoringPath[monitoringFullPath].exists(relativePath):
            #This item is not in the collection, so we need to extract info from this item
            newObj = self.dbInst.getFsObjFromFullPath(fullPath)
            self.collectionInDbForMonitoringPath[monitoringFullPath].addObj(relativePath, newObj["uuid"])
            for i in zippedInfo(self.workingDir).enumItems(fullPath):
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
        return True
    
if __name__ == "__main__":
    print 'starting fileListHandler'
    workingDir = "d:/tmp/working"
    s = zippedCollectionListHandler()
    s.startServer()