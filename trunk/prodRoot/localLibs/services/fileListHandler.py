'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import localLibSys
from localLibs.windows.changeNotifyThread import changeNotifyThread
import wwjufsdatabase.libs.utils.simplejson as json


gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileList"

class changeNotifyForBeanstalkd(changeNotifyThread):
    def callback(self, monitoringPath, fullPath, changeType):
        itemDict = {"monitoringPath": monitoringPath, "fullPath": fullPath, "changeType":changeType}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gMonitorServiceTubeName)
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)



class fileListService(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.notifyThreads = []
        pass
    def addItem(self, fullPath):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gFileListTubeName)
        itemDict = {"fullPath": fullPath}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)
    def startServer(self):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        #beanstalk.use(gFileListTubeName)
        beanstalk.watch(gFileListTubeName)
        beanstalk.ignore('default')
        while True:
            job = beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            #self.notifyThreads.append(changeNotifyForBeanstalkd(item["fullPath"]))
            
            
            
if __name__ == "__main__":
    print 'starting fileListHandler'
    s = fileListService()
    s.startServer()