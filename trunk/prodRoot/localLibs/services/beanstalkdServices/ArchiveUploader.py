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

class ArchiveUploader(FileListProcessorThreadBase):
        
    def process_file(self, file_obj, job):
        pass
    

        
class ArchiveUploadService(beanstalkServiceApp):
    def processItem(self, job, item):
        inputTubeName = item["input_tube_name"]
        target_dir = item["target_dir"]
        if self.is_processing_tube(inputTubeName):
            job.delete()
            return False
        t = ArchiveUploader(inputTubeName, target_dir)
        self.add_work_thread(inputTubeName, t)
        t.start()
        return True
    


if __name__ == "__main__":
    s = ArchiveUploadService()
    s.startServer()