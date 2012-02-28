'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os

#from pprint import pprint

import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json
from localLibs.storage.infoStorage.zippedCollectionWithInfo import zippedCollectionWithInfo
from localLibs.localFs.tmpFile import getStorgePathWithDateFolder
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"

gMaxZippedCollectionSize = 0.5*1024

gZipCollectionRoot = "d:/tmp/generating"

class fileListService(object):
    '''
    classdocs
    '''
    def __init__(self, zipCollectionRoot = gZipCollectionRoot, passwd = "123", workingDir = "d:/tmp/working", fileListTubeName = gFileListTubeName):
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
        self.fileListTubeName = fileListTubeName
        self.monitoringList = []
    '''
    def addItem(self, fullPath):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(self.fileListTubeName)
        itemDict = {"fullPath": fullPath}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)
    '''
    def startServer(self):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        #beanstalk.use(self.fileListTubeName)
        beanstalk.watch(self.fileListTubeName)
        beanstalk.ignore('default')
        while True:
            job = beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            if not os.path.exists(item["fullPath"]):
                print 'Path not exists'
                job.delete()
                continue
            if not (item['monitoringPath'] in self.monitoringList):
                self.monitoringList.append(item['monitoringPath'])
            info = self.storage.addItem(item["fullPath"])
            #print "zipped size", info.compress_size
            self.curStorageSize += info.compress_size
            self.addedList.append([job, item])
            if self.curStorageSize > gMaxZippedCollectionSize:
                self.storage.addAdditionalInfo({"monitoringPathList": self.monitoringList})
                zipFullPath = self.storage.finalizeZipFile()
                targetPath = getStorgePathWithDateFolder(self.zipCollectionRoot)
                self.encCopier.copy(zipFullPath, targetPath)
                self.monitoringList = []
                
                #print 'old file zipped, new file created'
                #pprint(beanstalk.stats_tube(self.fileListTubeName))
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