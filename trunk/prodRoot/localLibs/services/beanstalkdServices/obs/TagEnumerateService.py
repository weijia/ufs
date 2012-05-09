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


        
class TagEnumerateThread(beanstalkWorkingThread):
    '''
    input: {"tag":"", "output_tube_name":"", "target_dir":""}
    '''
    def __init__(self, input_tube_name, output_tube_name):
        super(TagEnumerateThread, self).__init__(input_tube_name)
        
    def processItem(self, job, item):
        
        
        #Must delete the job if it is no longer needed and return False so the job will not be put back to tube
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
                
                
class TagEnumerateService(beanstalkServiceApp):
    '''
    input: {"input_tube_name":"", "output_tube_name"}
    '''
    def processItem(self, job, item):
        input_tube_name = item["input_tube_name"]
        output_tube_name = item["output_tube_name"]
        
        self.taskDict[input_tube_name] = TagEnumerateThread(input_tube_name, output_tube_name)
        
        self.taskDict[input_tube_name].start()
        #Must delete the job if it is no longer needed and return False so the job will not be put back to tube
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True

if __name__ == "__main__":
    s = TagEnumerateService()
    s.startServer()