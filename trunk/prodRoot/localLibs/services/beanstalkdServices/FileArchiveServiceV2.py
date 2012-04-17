'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os
#import threading

#from pprint import pprint

import localLibSys
#from localLibs.storage.infoStorage.zippedCollectionWithInfo import zippedCollectionWithInfo
#from localLibs.storage.infoStorage.zippedInfoWithThumb import zippedInfoWithThumb
#from localLibs.localFs.tmpFile import getStorgePathWithDateFolder
#import localLibs.archiver.encryptionStorageBase as encryptionStorageBase
from beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp
import localLibs.objSys.objectDatabaseV3 as objectDatabase
import localLibs.utils.misc as misc
from localLibs.storage.infoCollectors.ThumbCollector import ThumbCollector
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.fileTools as fileTools
from localLibs.storage.archive.ZipFilesStorage import ZipFilesStorage

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"
gInfoFilePrefix = 'zippedCollFile'
gInfoFileExt = "log"
gMaxZippedCollectionSize = 0.005*1024

#g_working_dir = "d:/tmp/working/filearchivethread"

class FileArchiveThread(beanstalkWorkingThread):
    def __init__ ( self, input_tube_name, storage, collector_list, working_dir):
        '''
        Constructor
        '''
        super(FileArchiveThread, self).__init__(input_tube_name)
        self.storage = storage
        self.curStorageSize = 0
        self.monitoring_list = []
        self.dbInst = objectDatabase.objectDatabase()
        self.info_dict = {}
        self.collector_list = collector_list
        self.working_dir = working_dir

    def processItem(self, job, item):
        if not (item['monitoringPath'] in self.monitoring_list):
            self.monitoring_list.append(item['monitoringPath'])
            
        #Add item
        item_obj = self.dbInst.getFsObjFromFullPath(item["fullPath"])
        for collector in self.collector_list:
            addedItemSize = collector.collect_info(item_obj, self.info_dict, self.storage)   
            #print "zipped size", info.compress_size
            self.curStorageSize += addedItemSize
        #print "current size:", self.curStorageSize
        if self.curStorageSize > gMaxZippedCollectionSize:
            s = json.dumps(self.info_dict, sort_keys=True, indent=4)
            infoFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.working_dir, "."+gInfoFileExt, gInfoFilePrefix))
            logFile = open(infoFilePath, 'w')
            logFile.write(s)
            logFile.close()
            self.storage.add_file(infoFilePath)
            self.storage.finalize_one_trunk()
        return True
    

        
class FileArchiveService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, storage_class = ZipFilesStorage, collector_list = [ThumbCollector()], serviceControlTubeName = "fileArchiveServiceTubeName"):
        super(FileArchiveService, self).__init__(serviceControlTubeName)
        self.taskDict = {}
        self.storage_class = storage_class
        self.collector_list = collector_list

        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        workingDir = item["WorkingDir"]
        misc.ensureDir(workingDir)
        inputTubeName = item["InputTubeName"]
        target_dir = item["TargetDir"]
        if self.taskDict.has_key(inputTubeName):
            job.delete()
            return False
        t = FileArchiveThread(inputTubeName, self.storage_class(target_dir), self.collector_list, workingDir)
        self.taskDict[inputTubeName] = t
        t.start()
        return True
                

if __name__ == "__main__":
    #print 'starting fileListHandler'
    #workingDir = "d:/tmp/working"
    s = FileArchiveService()
    s.startServer()