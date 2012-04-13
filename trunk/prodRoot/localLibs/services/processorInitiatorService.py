'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import threading
import beanstalkc
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from beanstalkServiceBaseV2 import beanstalkServiceBase, beanstalkServiceApp

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
#gInputTubeName = "fileListTube"
#gOutputTubeName = "fileListDelayed"
gItemDelayTime = 5
gDefaultTtr = 3600*24
gDefaultTubeDelayServiceTubeName = 'tubeDelayServiceCmdTube'


class processorInitiatorService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gDefaultTubeDelayServiceTubeName):
        super(processorInitiatorService, self).__init__(tubeName)
        self.taskDict = {}
        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        blackList = item["blackList"]
        inputTubeName = item["inputTubeName"]
        outputTubeName = item["outputTubeName"]
        
        return True
            
            
            
            
if __name__ == "__main__":
    s = processorInitiatorService()
    s.startServer()