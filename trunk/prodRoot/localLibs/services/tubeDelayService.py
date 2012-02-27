'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import localLibSys
from localLibs.windows.changeNotifyThread import changeNotifyThread
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform


gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gInputTubeName = "fileList"
gOutputTubeName = "fileListDelayed"
gItemDelayTime = 5


class tubeDelayService(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.itemToProcess = {}
    def addItem(self, fullPath):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gInputTubeName)
        itemDict = {"fullPath": fullPath}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)
    def startServer(self):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        outputBeanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        #beanstalk.use(gMonitorServiceTubeName)
        beanstalk.watch(gInputTubeName)
        #beanstalk.ignore(gMonitorServiceTubeName)
        beanstalk.ignore('default')
        outputBeanstalk.use(gOutputTubeName)
        outputBeanstalk.ignore(gOutputTubeName)
        while True:
            job = beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            fullPath = transform.transformDirToInternal(item["fullPath"])
            #Check if item exists in local file sytem
            if not os.path.exists(fullPath):
                
                job.delete()
                continue
            
            #############################################
            # Start processing
            #############################################
            #If the full path already in tube, check if the timestamp is updated
            if self.itemToProcess.has_key(fullPath):
                savedItem = self.itemToProcess[fullPath]
                if savedItem["timestamp"] == item["timestamp"]:
                    #Item not updated for time out time, add it to output queue
                    outputBeanstalk.put(job.body)
                    print "output item:", item
                elif savedItem["timestamp"] < item["timestamp"]:
                    #Received a new notification for an path, update saved info
                    self.itemToProcess[fullPath] = item
                    job.release(delay = gItemDelayTime)
                    print "item updated"
                else:
                    job.delete()
            else:
                #New notification, add it
                self.itemToProcess[fullPath] = item
                job.release(delay = gItemDelayTime)
                print "new item added"
                
            
            
            
            
if __name__ == "__main__":
    s = tubeDelayService()
    s.startServer()