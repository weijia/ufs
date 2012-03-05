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

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
#gInputTubeName = "fileListTube"
#gOutputTubeName = "fileListDelayed"
gItemDelayTime = 5
gDefaultTtr = 3600*24


class zippedCollectionListHandler(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, inputTubeName):
        self.inputTubeName = inputTubeName
        super(zippedCollectionListHandler, self).__init__(inputTubeName)
        threading.Thread.__init__(self)
        
    def run(self):
        self.startServer()
            
    def processItem(self, job, item):
        monitoringFullPath = transform.transformDirToInternal(item['monitoringPath'])
        archiveId = "zippedInfoColllection://" + monitoringFullPath
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
        return True
            
            
class tubeDelayService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName):
        super(tubeDelayService, self).__init__(tubeName)
        self.taskDict = {}
        
    def processItem(self, job, item):
        inputTubeName = item["inputTubeName"]
        if not os.path.exists(inputTubeName) or self.taskDict.has_key(inputTubeName):
            job.delete()
        t = zippedCollectionListHandler(inputTubeName)
        self.taskDict[inputTubeName] = t
        t.start()
        #job.delete()
                
            
            
            
            
if __name__ == "__main__":
    s = tubeDelayService('tubeDelayServiceCmdTube')
    s.startServer()