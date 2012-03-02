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


class beanstalkServiceBase(object):
    '''
    classdocs
    '''
    def __init__(self, inputTubeName = gMonitorServiceTubeName):
        '''
        Constructor
        '''
        self.inputTubeName = inputTubeName
        
    def addItem(self, itemDict):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(self.inputTubeName)
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)
        
    def startServer(self):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.watch(self.inputTubeName)
        beanstalk.ignore('default')
        #!!!Not working. Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        while True:
            job = beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            print item
            if item.has_key('command'):
                self.processCmd(job, item)
            else:
                self.processItem(job, item)
    def processItem(self, job, item):
        job.delete()
    def processCmd(self, job, item):
        job.delete()
if __name__ == "__main__":
    s = beanstalkServiceBase()
    s.startServer()