'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os
#import threading

#from pprint import pprint

import localLibSys
from beanstalkServiceBaseV2 import beanstalkServiceApp
#import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *
from FileListProcessorThreadBase import FileListProcessorThreadBase
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.utils.misc as misc
import win32file


#g_working_dir = "d:/tmp/working/filearchivethread"


class CloudFolderStorage(object):
    def __init__(self, cloud_folder):
        super(CloudFolderStorage, self).__init__()
        self.cloud_folder = transform.transformDirToInternal(cloud_folder)
    def get_storage_id(self):
        return "CloudFolderStorage://"+self.cloud_folder
    def add_file(self, file_path):
        ext = os.path.splitext(file_path)
        target_path = misc.get_date_based_path(self.cloud_folder, ext)
        win32file.CreateSymbolicLink(file_path, target_path, 1)


g_file_archive_storage_collection_id = "uuid://e4d67513-08e4-40a5-9089-13fa67efcfc9"

class ArchiveUploader(FileListProcessorThreadBase):
        
    def process_file(self, file_obj, job):
        '''
        If the item should not be processed again, this method must add it to collection.
        '''
        #Copy the info to the new object.
        self.storage.add_file(file_obj.get_full_path())
        self.collection.addObj(file_obj.getObjUfsUrl(), file_obj.get_uuid())
        #
    

        
class ArchiveUploadService(beanstalkServiceApp):
    def processItem(self, job, item):
        inputTubeName = item["input_tube_name"]
        target_dir = item["target_dir"]
        if self.is_processing_tube(inputTubeName):
            job.delete()
            return False
        cloud_storage = CloudFolderStorage(target_dir)
        t = ArchiveUploader(inputTubeName, cloud_storage)
        self.add_work_thread(inputTubeName, t)
        t.start()
        return True
    def add_archive_target(self, input_tube_name, target_dir):
        self.addItem({"input_tube_name": input_tube_name, "target_dir": target_dir})

if __name__ == "__main__":
    s = ArchiveUploadService()
    s.startServer()