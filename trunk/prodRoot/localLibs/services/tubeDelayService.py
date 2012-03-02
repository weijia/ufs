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
from beanstalkServiceBase import beanstalkServiceBase

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gInputTubeName = "fileListTube"
gOutputTubeName = "fileListDelayed"
gItemDelayTime = 5
gDefaultTtr = 3600*24

class tubeDelayService(beanstalkServiceBase):
    '''
    classdocs
    '''
    def __init__(self, inputTubeName = gInputTubeName, outputTubeName = gOutputTubeName):
        '''
        Constructor
        '''
        super(tubeDelayService, self).__init__(inputTubeName)
        self.itemToProcess = {}
        self.outputTubeName = outputTubeName

    def processItem(self, job, item):
        outputBeanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        outputBeanstalk.use(self.outputTubeName)
        outputBeanstalk.ignore(self.outputTubeName)
        fullPath = transform.transformDirToInternal(item["fullPath"])
        #Check if item exists in local file sytem
        if not os.path.exists(fullPath):
            job.delete()
            return
        
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
                job.delete()
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
            #print item, job, gItemDelayTime
            '''
            print job.stats(), job.jid
            print type(gItemDelayTime)
            print "%d, %d"%(job.jid, gItemDelayTime)
            job.conn._interact('release %d %d %d\r\n' % (job.jid, beanstalkc.DEFAULT_PRIORITY, gItemDelayTime),
                       ['RELEASED', 'BURIED'],
                       ['NOT_FOUND'])
            '''
            job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
            print "new item added"
                
            
            
            
            
if __name__ == "__main__":
    s = tubeDelayService()
    s.startServer()