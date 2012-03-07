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

class tubeDelayThread(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, inputTubeName, outputTubeName, blackList = []):
        self.blackList = blackList
        self.outputTubeName = outputTubeName
        self.itemToProcess = {}
        super(tubeDelayThread, self).__init__(inputTubeName)
        threading.Thread.__init__(self)
        
    def run(self):
        self.outputBeanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        self.outputBeanstalk.use(self.outputTubeName)
        self.outputBeanstalk.ignore(self.outputTubeName)
        #self.outputBeanstalk.ignore('default')
        print 'Calling start server, output to: ', self.outputTubeName
        self.startServer()
            
    def processItem(self, job, item):
        monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        fullPath = transform.transformDirToInternal(item["fullPath"])
        #Check if item exists in local file sytem
        if not os.path.exists(fullPath):
            job.delete()
            return
        if not self.itemToProcess.has_key(monitoringFullPath):
            self.itemToProcess[monitoringFullPath] = {}
        #############################################
        # Start processing
        #############################################
        #If the full path already in tube, check if the timestamp is updated
        if self.itemToProcess[monitoringFullPath].has_key(fullPath):
            savedItem = self.itemToProcess[monitoringFullPath][fullPath]
            if savedItem["timestamp"] == item["timestamp"]:
                #Item not updated for time out time, add it to output queue
                self.outputBeanstalk.put(job.body)
                print "output item:", item
                job.delete()
            elif savedItem["timestamp"] < item["timestamp"]:
                #Received a new notification for an path, update saved info
                self.itemToProcess[monitoringFullPath][fullPath] = item
                job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
                print "item updated"
            else:
                job.delete()
        else:
            #New notification, add it
            self.itemToProcess[monitoringFullPath][fullPath] = item
            #print item, job, gItemDelayTime
            #priority is necessary to avoid error for requesting priority to be an int in beanstalkc
            job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
            print "new item added"
            
            
class tubeDelayService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gDefaultTubeDelayServiceTubeName):
        super(tubeDelayService, self).__init__(tubeName)
        self.taskDict = {}
        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        blackList = item["blackList"]
        inputTubeName = item["inputTubeName"]
        outputTubeName = item["outputTubeName"]
        if self.taskDict.has_key(inputTubeName):
            #Job already exist, delete it
            print "job already exist"
            job.delete()
            return False
        t = tubeDelayThread(inputTubeName, outputTubeName, blackList)
        self.taskDict[inputTubeName] = t
        t.start()
        return True
            
            
            
            
if __name__ == "__main__":
    s = tubeDelayService()
    s.startServer()