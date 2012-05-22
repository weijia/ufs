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

#g_file_archive_storage_collection_id = "uuid://e4d67513-08e4-40a5-9089-13fa67efcfc9"

class FileListProcessorThreadBase(beanstalkWorkingThread):
    def __init__ ( self, input_tube_name, storage):
        '''
        Constructor
        '''
        super(FileListProcessorThreadBase, self).__init__(input_tube_name)
        self.storage = storage
        self.curStorageSize = 0
        self.monitoring_list = []
        #self.dbInst = objectDatabase.objectDatabase()
        self.info_dict = {}
        self.collectionId = storage.get_storage_id()
        req = service.req()
        self.dbInst = req.getObjDbSys()
        self.collection = self.dbInst.getCollection(self.collectionId)
        #self.file_archive_collection = self.dbInst.getCollection(g_file_archive_storage_collection_id)
        #collection_virtual_obj_uuid = self.dbInst.addVirtualObj({"storage_collection_id":self.collectionId})
        #self.file_archive_collection.addObj(self.collectionId, collection_virtual_obj_uuid)
        #The following dictionary is used to update collection.
        #self.saving_items = {}
        
    def processItem(self, job, item):
        if not (item['monitoringPath'] in self.monitoring_list):
            self.monitoring_list.append(item['monitoringPath'])

        #Add item
        item_obj = self.dbInst.getFsObjFromFullPath(item["fullPath"])
        if not self.collection.exists(item_obj.getObjUfsUrl()):
            return self.process_file(item_obj, job)
            #return True#Return True will release the back to the tube
            
        else:
            job.delete()
            print "skipping item which is already in collection"
            return False#Do not need to put the item back to the tube

    def process_file(self):
        pass