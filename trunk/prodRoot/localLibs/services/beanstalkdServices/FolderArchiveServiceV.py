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

class FolderArchiveThread(beanstalkWorkingThread):
    def __init__ ( self, input_tube_name, storage, collector_list, working_dir):
        '''
        Constructor
        '''
        super(FolderArchiveThread, self).__init__(input_tube_name)
        self.storage = storage
        self.curStorageSize = 0
        #self.monitoring_list = []
        #self.dbInst = objectDatabase.objectDatabase()
        self.info_dict = {}
        self.collector_list = collector_list
        self.working_dir = working_dir
        self.collectionId = storage.get_storage_id()
        req = service.req()
        self.dbInst = req.getObjDbSys()
        self.collection = self.dbInst.getCollection(self.collectionId)
        
        #File Archive specific operations
        self.file_archive_collection = self.dbInst.getCollection(g_file_archive_storage_collection_id)
        collection_virtual_obj_uuid = self.dbInst.addVirtualObj({"storage_collection_id":self.collectionId})
        self.file_archive_collection.addObj(self.collectionId, collection_virtual_obj_uuid)
        #The following dictionary is used to update collection.
        self.saving_items = {}
        self.quit_flag = False
        
    def processItem(self, job, item):
        folder_root = item["folder_root"]
        cur_folder_path = item["current_folder_full_path"]
        obj_id_in_col = transform.getRelativePathFromFull(folder_root, cur_folder_path)
        folder_obj = self.obj_db.getFsObjFromFullPath(cur_folder_path)
        obj_uuid = folder_obj.get_uuid()
        res = self.collection.isSame(obj_id_in_col, obj_uuid)
        if not res:
            #The 2 folders are different
            #while(self.quit_flag):
            for file_element in os.listdir(cur_folder_path):
                full_path = os.path.join(cur_folder_path, file_element)
                self.ProcessFile(full_path)
                if self.quit_flag:
                    #break
                    return True
            return True#Return True will release the back to the tube
        else:
            job.delete()
            print "skipping item which is already in collection"
            return False#Do not need to put the item back to the tube
    def ProcessFile(self, full_path):
        #Add item
        item_obj = self.dbInst.getFsObjFromFullPath(full_path)
        if not self.collection.exists(item_obj.getObjUfsUrl()):
            for collector in self.collector_list:
                addedItemSize = collector.collect_info(item_obj, self.info_dict, self.storage)   
                info("saved size", addedItemSize)
                self.curStorageSize += addedItemSize
            info("current size:", self.curStorageSize)
            self.saving_items[item_obj.getObjUfsUrl()] = item_obj["uuid"]
            
            #Add dafault size for file basic info
            self.curStorageSize += gDefaultFileInfoSize
            
            if self.curStorageSize > gMaxZippedCollectionSize:
                info("size exceed max")
                self.finalize()
                self.curStorageSize = 0
            
            

    
    def finalize(self):
        #print self.info_dict
        #print len(self.info_dict)
        if len(self.info_dict) == 0:
            print "finalize without any content, return directly"
            return
        s = json.dumps(self.info_dict, sort_keys=True, indent=4)
        infoFilePath = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.working_dir, "."+gInfoFileExt, gInfoFilePrefix))
        logFile = open(infoFilePath, 'w')
        logFile.write(s)
        logFile.close()
        #print s
        info(infoFilePath)
        self.storage.add_file(infoFilePath)
        self.storage.finalize_one_trunk()
        for i in self.saving_items:
            self.collection.addObj(i, self.saving_items[i])
        self.saving_items = {}
        self.info_dict = {}
        info("trunk finalized")

    def stop(self):
        self.finalize()
        print "file archive service stop called"
        
    #############################
    # The following function will be called from outside of this.
    # So it must be thread safe
    #############################
    def external_stop(self):
        self.quit_flag = True
    


from localLibs.compress.EncZipFileOn7Zip import EncZipFileOn7Zip
gWorkingDir = "d:/tmp/working/zipfilestorage"
import win32file
import traceback
import shutil

class SyncedCompressedStorage(CompressedStorage):
    def __init__(self, trunk_data_path = gWorkingDir, package_class = EncZipFileOn7Zip, 
                 ext = ".7z", passwd = '123', sync_folder = "d:/tmp/working/sync"):
        super(SyncedCompressedStorage, self).__init__(trunk_data_path, package_class, 
                                                ext, passwd)
        self.sync_folder = sync_folder
    def finalize_one_trunk(self):
        trunk_path = super(SyncedCompressedStorage, self).finalize_one_trunk()
        root, ext = os.path.splitext(trunk_path)
        target_path = misc.get_date_based_path(self.sync_folder, ext)
        req = service.req()
        cache_db = req.getDbSys().getDb("cache_db")
        obj_db = req.getObjDbSys()
        obj = obj_db.getFsObjFromFullPath(trunk_path)
        obj_uuid = obj.get_uuid()
        cache_db.append(obj_uuid, target_path)
        try:
            win32file.CreateSymbolicLink(trunk_path, target_path, 1)
        except:
            traceback.print_exc()
            shutil.copyfile(trunk_path, target_path)
    def get_storage_id(self):
        return "zip_file_storage://"+transform.transformDirToInternal(self.sync_folder)

        
class FolderArchiveService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, storage_class = SyncedCompressedStorage, collector_list = [ThumbCollector()], serviceControlTubeName = "fileArchiveServiceTubeName", passwd = "123"):
        super(FolderArchiveService, self).__init__(serviceControlTubeName)
        self.storage_class = storage_class
        self.collector_list = collector_list
        self.passwd = passwd

        
    def processItem(self, job, item):
        working_dir = item["WorkingDir"]
        misc.ensureDir(working_dir)
        
        tmp_file_path = os.path.join(working_dir, "tmp_file_path")
        misc.ensureDir(tmp_file_path)

        other_tmp_file_path = os.path.join(working_dir, "other_tmp_file_path")
        misc.ensureDir(other_tmp_file_path)        
        
        
        inputTubeName = item["InputTubeName"]
        target_dir = item["TargetDir"]
        if self.is_processing_tube(inputTubeName):
            job.delete()
            return False
        t = FolderArchiveThread(inputTubeName, 
                              self.storage_class(tmp_file_path, 
                                                 passwd=self.passwd, 
                                                 sync_folder = target_dir), 
                              self.collector_list, other_tmp_file_path)
        self.add_work_thread(inputTubeName, t)
        t.start()
        return True
    def stop(self):
        super(FolderArchiveService, self).stop()
        for input_channel_name in self.input_channel_name_to_work_thread_dict:
            self.input_channel_name_to_work_thread_dict[input_channel_name]


if __name__ == "__main__":
    #print 'starting fileListHandler'
    #workingDir = "d:/tmp/working"
    passwd = "123qwe"
    from localLibs.utils.misc import get_prot_root
    passwd_file = os.path.join(get_prot_root(), "passwd.config")
    if os.path.exists(passwd_file):
        f = open(passwd_file)
        passwd = f.read().replace("\r","").replace("\n", "")
        f.close()
    #print "passwd: ", passwd
    s = FileArchiveService(passwd = passwd)
    s.startServer()