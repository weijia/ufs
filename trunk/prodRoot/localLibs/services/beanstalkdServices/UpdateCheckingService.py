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

class UpdateCheckingThread(beanstalkWorkingThread):
    def __init__ ( self, tubeName, rootFolder, state_collection_id, blackList = []):
        self.blackList = blackList
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        super(UpdateCheckingThread, self).__init__ (tubeName)
        self.quit_flag = False
        import wwjufsdatabase.libs.services.servicesV2 as service
        self.req = service.req()
        self.obj_db = self.req.getObjDbSys()
        self.collection = self.obj_db.getCollection(state_collection_id)
    
    def add_to_collection(self, full_path):
        '''
        Return true if the item is already in collection
        '''
        full_path = transform.transformDirToInternal(full_path)
        obj_id_in_col = transform.getRelativePathFromFull(full_path, self.rootFolder)
        dir_obj = self.obj_db.getFsObjFromFullPath(full_path)
        obj_uuid = dir_obj.get_uuid()
        res = self.collection.isSame(obj_id_in_col, obj_uuid)
        if not res:
            cl("updated:", obj_uuid, obj_id_in_col)
            self.collection.addObj(obj_id_in_col, dir_obj.get_uuid())
        else:
            #cl("not updated:", obj_uuid, obj_id_in_col)
            pass
        return res
            

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
                if self.quit_flag:
                    break
                #Process dirs, ignore not updated dirs, must not remove when enumerating
                already_in_collection = []
                for dir in dirs:
                    if self.add_to_collection(os.path.join(root, dir)):
                        info("ignoring: ", os.path.join(root, dir), "\n")
                        already_in_collection.append(dir)
                for i in already_in_collection:
                    dirs.remove(i)
                #cl("remaining:", dirs)
                #Process files
                for j in files:
                    info(j)
                    if filter(j, self.blackList):
                        info("ignoring: ", j, "\n")
                        continue
                    
                    fullPath = transform.transformDirToInternal(os.path.join(root, j))
                    if self.add_to_collection(fullPath):
                        info("ignoring: ", fullPath, "\n")
                        continue
                    
                    paramDict = {"fullPath": fullPath, "timestamp": os.stat(fullPath)[ST_MTIME],
                                 "monitoringPath": self.rootFolder}
                    self.addItem(paramDict)
        print "process complete, quitting thread"
    def stop(self):
        self.quit_flag = True

class UpdateCheckingService(beanstalkServiceApp):
    '''
    service request format:
    {"full_path":"", "black_list":"", "target_tube_name":"", "state_collection_id":""
    }
    '''
    def __init__(self, tubeName = None):
        '''
        Constructor
        '''
        super(UpdateCheckingService, self).__init__(tubeName)
        ##############################
        # The thread should be value not the key, input tube should be the key
        ##############################
        
    def processItem(self, job, item):
        fullPath = transform.transformDirToInternal(item["full_path"])
        blackList = item["black_list"]
        targetTubeName = item["target_tube_name"]
        state_collection_id = item["state_collection_id"]
        if not os.path.exists(fullPath):
            print "Path not exist: ", fullPath
            job.delete()
            return False#Job Deleted
        if self.is_processing_tube(fullPath):
            print "Already scanning path: ", fullPath
            job.delete()
            return False#Job Deleted
        thread_instance = UpdateCheckingThread(targetTubeName, fullPath, state_collection_id, blackList)
        self.add_work_thread(fullPath, thread_instance)
        print 'Starting new working thread'
        thread_instance.start()
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
        
        
if __name__ == "__main__":
    s = UpdateCheckingService()
    s.startServer()