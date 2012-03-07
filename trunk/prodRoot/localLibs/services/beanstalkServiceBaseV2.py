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
gMonitorServiceTubeName = "monitorQueue"
gItemDelayTime = 60*60*24#One day

class beanstalkServiceBase(object):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gMonitorServiceTubeName):
        '''
        Constructor
        '''
        self.tubeName = tubeName
        self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        
    def addItem(self, itemDict):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(self.tubeName)
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        print "add item:", s, self.tubeName
        job = beanstalk.put(s)
        
    def watchTube(self):
        self.beanstalk.watch(self.tubeName)
        self.beanstalk.ignore('default')
        
        
class beanstalkServiceApp(beanstalkServiceBase):
    def startServer(self):
        print self.__class__, self.tubeName
        self.watchTube()
        #!!!Not working. Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        while True:
            job = self.beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            print item
            try:
                if self.processItem(job, item):
                    #If return True, the job was processed, release and delay it
                    job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
            except Exception,e:
                print e
                raise e
                #job.delete()
    def processItem(self, job, item):
        job.delete()

        
if __name__ == "__main__":
    s = beanstalkServiceBase()
    s.startServer()