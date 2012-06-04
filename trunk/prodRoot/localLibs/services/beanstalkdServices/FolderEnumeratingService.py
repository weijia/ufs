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




def filter(filepath, filter_list):
    for i in filter_list:
        if re.search("\." + i.split(".")[1] + "$", i) is None:
            return True
        else:
            return False

class FolderEnumeratingThread(beanstalkWorkingThread):
    def __init__ ( self, tubeName, rootFolder, blackList = []):
        self.blackList = blackList
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        super(FolderEnumeratingThread, self).__init__ (tubeName)
        self.quit_flag = False
        import wwjufsdatabase.libs.services.servicesV2 as service
        self.req = service.req()
        self.obj_db = self.req.getObjDbSys()
    
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
            for root, dirs, files in os.walk(self.rootFolder):
                #Break if quit called
                if self.quit_flag:
                    break
                #cl("remaining:", dirs)
                #Process files
                for j in dirs:
                    info(j)
                    if filter(j, self.blackList):
                        info("ignoring: ", j, "\n")
                        continue
                    
                    fullPath = transform.transformDirToInternal(os.path.join(root, j))

                    paramDict = {"fullPath": fullPath, "timestamp": os.stat(fullPath)[ST_MTIME],
                                 "monitoringPath": self.rootFolder}
                    self.addItem(paramDict)
        print "process complete, quitting thread"


class FolderEnumeratingService(beanstalkServiceApp):
    '''
    service request format:
    {"full_path":"", "black_list":"", "target_tube_name":""
    }
    '''
    def __init__(self, tubeName = None):
        '''
        Constructor
        '''
        super(FolderEnumeratingService, self).__init__(tubeName)
        ##############################
        # The thread should be value not the key, input tube should be the key
        ##############################
        
    def processItem(self, job, item):
        fullPath = transform.transformDirToInternal(item["full_path"])
        blackList = item["black_list"]
        targetTubeName = item["target_tube_name"]
        if not os.path.exists(fullPath):
            print "Path not exist: ", fullPath
            job.delete()
            return False#Job Deleted
        if self.is_processing_tube(fullPath):
            print "Already scanning path: ", fullPath
            job.delete()
            return False#Job Deleted
        thread_instance = FolderEnumeratingThread(targetTubeName, fullPath, blackList)
        self.add_work_thread(fullPath, thread_instance)
        print 'Starting new working thread'
        thread_instance.start()
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
        
        
if __name__ == "__main__":
    s = FolderEnumeratingService()
    s.startServer()