'''
Created on 2012-05-09

@author: Richard
'''
import beanstalkc
import os

#from pprint import pprint

import localLibSys
from localLibs.services.clients.zippedCollectionListHandlerThumbClientV2 import AutoArchiveThumb
from beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp
import localLibs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform 


        
class AutoExtractInfoWithThumbThread(beanstalkWorkingThread):
    '''
    input: {"source_dir":"", "working_dir":"", "target_dir":""}
    '''
        
    def processItem(self, job, item):
        source_dir = item["source_dir"]
        if os.path.isdir(source_dir):
            misc.ensureDir(transform.transformDirToInternal(source_dir))
        
        working_dir = item["working_dir"]
        misc.ensureDir(transform.transformDirToInternal(working_dir))
        
        target_dir = item["target_dir"]
        misc.ensureDir(transform.transformDirToInternal(target_dir))
        
        sync_folder = item["sync_folder"]
        misc.ensureDir(transform.transformDirToInternal(sync_folder))

        AutoArchiveThumb(source_dir, target_dir, working_dir, sync_folder)
        
        #Must delete the job if it is no longer needed and return False so the job will not be put back to tube
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
                
                
class AutoExtractInfoWithThumbeService(beanstalkServiceApp):
    '''
    input: {"input_tube_name":""}
    '''
    def processItem(self, job, item):
        input_tube_name = item["input_tube_name"]
        
        t = AutoExtractInfoWithThumbThread(input_tube_name)
        self.add_work_thread(input_tube_name, t)
        
        t.start()
        #Must delete the job if it is no longer needed and return False so the job will not be put back to tube
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True

if __name__ == "__main__":
    s = AutoExtractInfoWithThumbeService()
    s.startServer()