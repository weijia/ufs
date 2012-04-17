'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc


#from pprint import pprint

import localLibSys
from localLibs.storage.infoStorage.zippedCollectionWithInfo import zippedCollectionWithInfo
from localLibs.services.clients.zippedCollectionListHandlerThumbClientV2 import AutoArchiveThumb
from beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp
import localLibs.utils.misc as misc



        
class AutoProcessService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = "AutoProcessServiceTubeName"):
        super(AutoProcessService, self).__init__(tubeName)
        self.taskDict = {}

        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        working_dir = item["WorkingDir"]
        misc.ensureDir(working_dir)
        
        source_dir = item["SourceDir"]
        misc.ensureDir(source_dir)
        
        target_dir = item["TargetDir"]
        misc.ensureDir(target_dir)
        
        AutoArchiveThumb(source_dir, target_dir, working_dir)
        return True
                

if __name__ == "__main__":
    s = AutoProcessService()
    s.startServer()