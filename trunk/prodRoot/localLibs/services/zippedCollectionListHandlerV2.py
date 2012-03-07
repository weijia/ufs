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
import wwjufsdatabase.libs.utils.simplejson as json
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

class zippedCollectionListHandler(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, tubeName, workingDir = "d:/tmp/working/zippedCollectionListHandler"):
        super(zippedCollectionListHandler, self).__init__(tubeName)
        threading.Thread.__init__(self)
        self.collectionDict = {}
        self.dbInst = objectDatabase.objectDatabase()
        self.workingDir = workingDir
    def run(self):
        self.startServer()
            
    def processItem(self, job, item):
        monitoringFullPath = transform.transformDirToInternal(item['monitoringPath'])
        archiveId = gZipFolderCollectionPrefix + monitoringFullPath
        if not self.collectionDict.has_key(monitoringFullPath):
            self.collectionDict[monitoringFullPath] = collectionDatabase.collectionOnMongoDbBase(archiveId, self.dbInst.getCollectionDb())
        #Save the item in the archive collection: zippedInfoColllection://D:/tmp/
        fullPath = transform.transformDirToInternal(item["fullPath"])
        relativePath = transform.getRelativePathFromFull(fullPath, monitoringFullPath)
        if not self.collectionDict[monitoringFullPath].exists(relativePath):
            #This item is not in the collection, so we need to extract info from this item
            newObj = self.dbInst.getFsObjFromFullPath(fullPath)
            self.collectionDict[monitoringFullPath].addObj(relativePath, newObj["uuid"])
            for i in zippedInfo(self.workingDir).enumItems(fullPath):
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
            for i in zippedInfo(self.workingDir).enumZippedFiles(fullPath):
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
        else:
            #This item is not in the collection, so we need to extract info from this item
            newObj = self.dbInst.getFsObjFromFullPath(fullPath)
            self.collectionDict[monitoringFullPath].addObj(relativePath, newObj["uuid"])
            for i in zippedInfo(self.workingDir).enumItems(fullPath):
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
            for i in zippedInfo(self.workingDir).enumZippedFiles(fullPath):
                fp = open(i, 'r')
                loadedFileInfo = json.load(fp)
                print loadedFileInfo
        return True
            
            
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