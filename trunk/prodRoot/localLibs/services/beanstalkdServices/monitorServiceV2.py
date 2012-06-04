'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import localLibSys
from localLibs.windows.changeNotifyThread import changeNotifyThread
import wwjufsdatabase.libs.utils.transform as transform
from beanstalkServiceBaseV2 import beanstalkServiceApp
import wwjufsdatabase.libs.utils.simplejson as json

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileList"
gMaxMonitoringItems = 100

class changeNotifyForBeanstalkd(changeNotifyThread):
    def __init__(self, fullPath, targetTube, blackList = []):
        super(changeNotifyForBeanstalkd, self).__init__(fullPath)
        self.blackList = blackList
        self.targetTube = targetTube
    def callback(self, pathToWatch, relativePath, changeType):
        fullPath = transform.transformDirToInternal(os.path.join(pathToWatch, relativePath))
        itemDict = {"monitoringPath": transform.transformDirToInternal(pathToWatch),
                        "fullPath": fullPath, "changeType":changeType,
                        "timestamp": time.time()}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(self.targetTube)
        #print beanstalk.using()
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)



class monitorService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = gMonitorServiceTubeName):
        '''
        Constructor
        '''
        super(monitorService, self).__init__(tubeName)
        self.notifyThreads = {}

    def processItem(self, job, item):
        fullPath = transform.transformDirToInternal(item["fullPath"])
        blackList = item["blackList"]
        targetTube = item["targetTubeName"]
        if not os.path.exists(fullPath) or self.notifyThreads.has_key(fullPath):
            job.delete()
            return False
        if not os.path.isdir(fullPath):
            cl("file change is not supported yet:", fullPath)
            job.delete()
            return False
        t = changeNotifyForBeanstalkd(fullPath, targetTube, blackList)
        self.notifyThreads[fullPath] = t
        t.start()
        return True

if __name__ == "__main__":
    s = monitorService()
    s.startServer()