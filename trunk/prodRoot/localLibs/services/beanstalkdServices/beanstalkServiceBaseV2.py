'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import traceback
import threading

import localLibSys
from localLibs.windows.changeNotifyThread import changeNotifyThread
import wwjufsdatabase.libs.utils.simplejson as json
import localLibs.server.XmlRpcServer2BeanstalkdServiceBridge as bridge

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
        print 'watch tube: ', self.tubeName
        self.beanstalk.watch(self.tubeName)
        self.beanstalk.ignore('default')
        
        
class beanstalkServiceApp(beanstalkServiceBase):
    def __init__(self, tube_name):
        super(beanstalkServiceApp, self).__init__(tube_name)
        bridge.subscribe(tube_name)
        
        
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
            if item.has_key("command"):
                if item["command"] == "quit":
                    print "got a quit message"
                    self.stop()
                    job.delete()
                    #return
                    continue
            print item
            try:
                if self.processItem(job, item):
                    #If return True, the job was processed but should be still in queue, release and delay it
                    job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
            except Exception,e:
                traceback.print_exc()
                #raise e
                #job.delete()
    def processItem(self, job, item):
        job.delete()
        return False#Return False if we do not need to put the item back to tube
    
    def stop(self):
        print "got a quit message"


class beanstalkWorkingThread(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, inputTubeName):
        super(beanstalkWorkingThread, self).__init__(inputTubeName)
        threading.Thread.__init__(self)
    def run(self):
        self.startServer()
        
if __name__ == "__main__":
    s = beanstalkServiceBase()
    s.startServer()