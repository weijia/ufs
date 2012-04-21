'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from beanstalkServiceBaseV2 import beanstalkServiceApp
import threading
from stat import *

gFolderScannerTubeName = "folderScannerTube"

class folderScannerThread(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, tubeName, rootFolder, blackList = []):
        self.blackList = blackList
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        super(folderScannerThread, self).__init__ (tubeName)
        threading.Thread.__init__(self)
        
    def run(self):
        print 'Start scanning'
        if not os.path.isdir(self.rootFolder):
            print "not a folder"
            paramDict = {"fullPath": self.rootFolder, "timestamp": os.stat(self.rootFolder)[ST_MTIME],
                             "monitoringPath": self.rootFolder}
            self.addItem(paramDict)
        else:
            for i in os.walk(self.rootFolder):
                for j in i[2]:
                    print j
                    fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
                    paramDict = {"fullPath": fullPath, "timestamp": os.stat(fullPath)[ST_MTIME],
                                 "monitoringPath": self.rootFolder}
                    self.addItem(paramDict)

class folderScanner(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gFolderScannerTubeName):
        '''
        Constructor
        '''
        super(folderScanner, self).__init__(tubeName)
        self.scannerThreadDict = {}
        
    def processItem(self, job, item):
        fullPath = transform.transformDirToInternal(item["fullPath"])
        blackList = item["blackList"]
        targetTubeName = item["targetTubeName"]
        if not os.path.exists(fullPath) or self.scannerThreadDict.has_key(fullPath):
            print "Path not exist: ", fullPath
            job.delete()
            return False#Job Deleted
        t = folderScannerThread(targetTubeName, fullPath, blackList)
        self.scannerThreadDict[fullPath] = t
        print 'Starting new working thread'
        t.start()
        job.delete()
        return False
        #return True
        
        
if __name__ == "__main__":
    s = folderScanner(gFolderScannerTubeName)
    s.startServer()