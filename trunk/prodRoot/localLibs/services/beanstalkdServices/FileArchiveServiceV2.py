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
#import localLibs.objSys.objectDatabaseV3 as objectDatabase
import localLibs.utils.misc as misc
from localLibs.storage.infoCollectors.ThumbCollector import ThumbCollector
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.fileTools as fileTools
from localLibs.storage.archive.CompressedStorage import CompressedStorage
import wwjufsdatabase.libs.services.servicesV2 as service
from localLibs.logSys.logSys import *

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"
gInfoFilePrefix = 'zippedCollFile'
gInfoFileExt = "log"
gMaxZippedCollectionSize = 2*1024*1024
gDefaultFileInfoSize = 20

#g_working_dir = "d:/tmp/working/filearchivethread"

g_file_archive_storage_collection_id = "uuid://e4d67513-08e4-40a5-9089-13fa67efcfc9"

class FileArchiveThread(beanstalkWorkingThread):
    def __init__ ( self, input_tube_name, storage, collector_list, working_dir):
        '''
        Constructor
        '''
        super(FileArchiveThread, self).__init__(input_tube_name)
        self.storage = storage
        self.curStorageSize = 0
        self.monitoring_list = []
        #self.dbInst = objectDatabase.objectDatabase()
        self.info_dict = {}
        self.collector_list = collector_list
        self.working_dir = working_dir
        self.collectionId = storage.get_storage_id()
        req = service.req()
        self.dbInst = req.getObjDbSys()
        self.collection = self.dbInst.getCollection(self.collectionId)
        self.file_archive_collection = self.dbInst.getCollection(g_file_archive_storage_collection_id)
        collection_virtual_obj_uuid = self.dbInst.addVirtualObj({"storage_collection_id":self.collectionId})
        self.file_archive_collection.addObj(self.collectionId, collection_virtual_obj_uuid)
        self.saving_items = {}
        
    def processItem(self, job, item):
        if not (item['monitoringPath'] in self.monitoring_list):
            self.monitoring_list.append(item['monitoringPath'])

        #Add item
        item_obj = self.dbInst.getFsObjFromFullPath(item["fullPath"])
        if not self.collection.exists(item_obj.getObjUfsUrl()):
            for collector in self.collector_list:
                addedItemSize = collector.collect_info(item_obj, self.info_dict, self.storage)   
                print "zipped size", addedItemSize
                self.curStorageSize += addedItemSize
            print "current size:", self.curStorageSize
            self.saving_items[item_obj.getObjUfsUrl()] = item_obj["uuid"]
            
            #Add dafault size for file basic info
            self.curStorageSize += gDefaultFileInfoSize
            
            if self.curStorageSize > gMaxZippedCollectionSize:
                cl("size exceed max")
                self.finalize()
                self.curStorageSize = 0
            return True#Return True will release the back to the tube
            
        else:
            job.delete()
            print "skipping item which is already in collection"
            return False#Do not need to put the item back to the tube
    
    def finalize(self):
        if len(self.saving_items) == 0:
            print "finalize without any content, return directly"
            return
        s = json.dumps(self.info_dict, sort_keys=True, indent=4)
        infoFilePath = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.working_dir, "."+gInfoFileExt, gInfoFilePrefix))
        logFile = open(infoFilePath, 'w')
        logFile.write(s)
        logFile.close()
        info(infoFilePath)
        self.storage.add_file(infoFilePath)
        self.storage.finalize_one_trunk()
        for i in self.saving_items:
            self.collection.addObj(i, self.saving_items[i])
        self.saving_items = {}
        print "trunk finalized"

    def stop(self):
        self.finalize()
        print "file archive service stop called"
        
class FileArchiveService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, storage_class = CompressedStorage, collector_list = [ThumbCollector()], serviceControlTubeName = "fileArchiveServiceTubeName", passwd = "123"):
        super(FileArchiveService, self).__init__(serviceControlTubeName)
        self.taskDict = {}
        self.storage_class = storage_class
        self.collector_list = collector_list
        self.passwd = passwd

        
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
        t = FileArchiveThread(inputTubeName, self.storage_class(target_dir, passwd=self.passwd), self.collector_list, workingDir)
        self.taskDict[inputTubeName] = t
        t.start()
        return True
    


if __name__ == "__main__":
    #print 'starting fileListHandler'
    #workingDir = "d:/tmp/working"
    passwd = "123"
    from localLibs.utils.misc import get_prot_root
    passwd_file = os.path.join(get_prot_root(), "passwd.config")
    if os.path.exists(passwd_file):
        f = open(passwd_file)
        passwd = f.read().replace("\r","").replace("\n", "")
        f.close()
    #print "passwd: ", passwd
    s = FileArchiveService(passwd = passwd)
    s.startServer()