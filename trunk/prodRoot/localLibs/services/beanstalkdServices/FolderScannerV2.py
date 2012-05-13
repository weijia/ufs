'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from beanstalkServiceBaseV2 import beanstalkServiceApp, beanstalkWorkingThread
import threading
from stat import *
from localLibs.logSys.logSys import *
import re

gFolderScannerTubeName = "folderScannerTube"

def filter(filepath, filter_list):
    for i in filter_list:
        if re.search("\." + i.split(".")[1] + "$", i) is None:
            return True
        else:
            return False

class FolderScannerThread(beanstalkWorkingThread):
    def __init__ ( self, tubeName, rootFolder, blackList = []):
        self.blackList = blackList
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        super(FolderScannerThread, self).__init__ (tubeName)
        self.quit_flag = False
        
    def run(self):
        print 'Start scanning'
        if not os.path.isdir(self.rootFolder):
            print "not a folder"
            if filter(self.rootFolder, self.blackList):
                return
            paramDict = {"fullPath": self.rootFolder, "timestamp": os.stat(self.rootFolder)[ST_MTIME],
                             "monitoringPath": self.rootFolder}
            self.addItem(paramDict)
        else:
            for i in os.walk(self.rootFolder):
                if self.quit_flag:
                    break
                for j in i[2]:
                    info(j)
                    if filter(j, self.blackList):
                        info("ignoring: ", j)
                        continue
                    fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
                    paramDict = {"fullPath": fullPath, "timestamp": os.stat(fullPath)[ST_MTIME],
                                 "monitoringPath": self.rootFolder}
                    self.addItem(paramDict)
    def stop(self):
        self.quit_flag = True

class FolderScanner(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gFolderScannerTubeName):
        '''
        Constructor
        '''
        super(FolderScanner, self).__init__(tubeName)
        self.scannerThreadDict = {}
        
    def processItem(self, job, item):
        fullPath = transform.transformDirToInternal(item["fullPath"])
        blackList = item["blackList"]
        targetTubeName = item["targetTubeName"]
        if not os.path.exists(fullPath) or self.scannerThreadDict.has_key(fullPath):
            print "Path not exist: ", fullPath
            job.delete()
            return False#Job Deleted
        t = FolderScannerThread(targetTubeName, fullPath, blackList)
        self.scannerThreadDict[fullPath] = t
        print 'Starting new working thread'
        t.start()
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
    def stop(self):
        for i in self.scannerThreadDict:
            self.scannerThreadDict[i].stop()
        
        
if __name__ == "__main__":
    s = FolderScanner(gFolderScannerTubeName)
    s.startServer()