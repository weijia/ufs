'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from beanstalkServiceBase import beanstalkServiceBase
import threading
from stat import *

gFolderScannerTubeName = "folderScannerTube"

class folderScannerThread(threading.Thread):
    def __init__ ( self, rootFolder, targetTubeName, blackList = []):
        self.blackList = blackList
        self.targetTube = beanstalkServiceBase(targetTubeName)
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        super(folderScannerThread, self).__init__ ()
        
    def run(self):
        for i in os.walk(self.rootFolder):
            for j in i[2]:
                fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
                paramDict = {"fullPath": fullPath, "timestamp": os.stat(fullPath)[ST_MTIME],
                             "monitoringPath": self.rootFolder}
                self.targetTube.addItem(paramDict)

class folderScanner(beanstalkServiceBase):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gFolderScannerTubeName):
        '''
        Constructor
        '''
        super(folderScanner, self).__init__(tubeName)
        self.scannerThreadDict = {}
        
    def processCmd(self, job, item):
        fullPath = transform.transformDirToInternal(item["fullPath"])
        blackList = item["blackList"]
        targetTubeName = item["targetTubeName"]
        if not os.path.exists(fullPath) or self.scannerThreadDict.has_key(fullPath):
            job.delete()
        t = folderScannerThread(fullPath, targetTubeName, blackList)
        self.scannerThreadDict[fullPath] = t
        t.start()
        
        
if __name__ == "__main__":
    s = folderScanner(gFolderScannerTubeName)
    s.startServer()