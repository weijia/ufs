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
gFileListTubeName = "fileList"
gMaxMonitoringItems = 100

class changeNotifyForBeanstalkd(changeNotifyThread):
    def callback(self, pathToWatch, relativePath, changeType):
        fullPath = transform.transformDirToInternal(os.path.join(pathToWatch, relativePath))
        itemDict = {"monitoringPath": transform.transformDirToInternal(pathToWatch),
                        "fullPath": fullPath, "changeType":changeType,
                        "timestamp": time.time()}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gFileListTubeName)
        #print beanstalk.using()
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)



class monitorService(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.notifyThreads = {}
        pass
    def addItem(self, fullPath):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gMonitorServiceTubeName)
        itemDict = {"fullPath": fullPath}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)
    def startServer(self):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        #beanstalk.use(gMonitorServiceTubeName)
        beanstalk.watch(gMonitorServiceTubeName)
        #beanstalk.ignore(gMonitorServiceTubeName)
        beanstalk.ignore('default')
        #!!!Not working. Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        while True:
            job = beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            fullPath = transform.transformDirToInternal(item["fullPath"])
            if self.notifyThreads.has_key(fullPath):
                #Notifier already added.
                continue
            if not os.path.exists(item["fullPath"]) or self.notifyThreads.has_key(fullPath):
                job.delete()
                continue
            t = changeNotifyForBeanstalkd(fullPath)
            self.notifyThreads[fullPath] = t
            t.start()
            #job.bury()
            
            
if __name__ == "__main__":
    s = monitorService()
    s.startServer()