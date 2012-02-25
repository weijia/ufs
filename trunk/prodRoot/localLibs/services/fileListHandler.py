'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os

from pprint import pprint

import localLibSys
from localLibs.windows.changeNotifyThread import changeNotifyThread
import wwjufsdatabase.libs.utils.simplejson as json
from localLibs.storage.infoStorage.zippedCollectionWithInfo import zippedCollectionWithInfo
from localLibs.localFs.tmpFile import getStorgePathWithDateFolder
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileList"

gMaxZippedCollectionSize = 0.5*1024

class changeNotifyForBeanstalkd(changeNotifyThread):
    def callback(self, monitoringPath, fullPath, changeType):
        itemDict = {"monitoringPath": monitoringPath, "fullPath": fullPath, "changeType":changeType}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gMonitorServiceTubeName)
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)

gZipCollectionRoot = "d:/tmp/generating"

class fileListService(object):
    '''
    classdocs
    '''
    def __init__(self, zipCollectionRoot = gZipCollectionRoot, passwd = "123", workingDir = "d:/tmp/working"):
        '''
        Constructor
        '''
        self.notifyThreads = []
        self.storage = zippedCollectionWithInfo(workingDir)
        self.zipCollectionRoot = zipCollectionRoot
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        self.curStorageSize = 0
        self.addedList = []
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
            if not os.path.exists(item["fullPath"]):
                print 'Path not exists'
                job.delete()
                continue
            info = self.storage.addItem(item["fullPath"])
            #print "zipped size", info.compress_size
            self.curStorageSize += info.compress_size
            self.addedList.append([job, item])
            if self.curStorageSize > gMaxZippedCollectionSize:
                zipFullPath = self.storage.finalizeZipFile()
                targetPath = getStorgePathWithDateFolder(self.zipCollectionRoot)
                self.encCopier.copy(zipFullPath, targetPath)
                print 'old file zipped, new file created'
                #pprint(beanstalk.stats_tube(gFileListTubeName))
                #print self.addedList
                for addedJob, addedItem in self.addedList:
                    #print dir(addedJob)
                    #print addedJob.state()
                    try:
                        addedJob.delete()
                    except:
                        pass
                    print "removed addedItem from tube", addedItem
                self.addedList = []
                #TODO: Remove tmp file.
            
if __name__ == "__main__":
    print 'starting fileListHandler'
    s = fileListService()
    s.startServer()