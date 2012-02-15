'''
Created on 2011-9-23

@author: Richard
'''
#import threading
import xmlrpclib
import localLibSys
import xmlRpcServerWithWorkerThreadBase
import localLibs.localTasks.collectionSync as collectionSync
from localLibs.logSys.logSys import *

class syncThread(xmlRpcServerWithWorkerThreadBase.serverThread):
    def __init__(self, taskUuid, folderPath, encZipPath, passwd, workingPath):
        xmlRpcServerWithWorkerThreadBase.serverThread.__init__(self)
        self.taskUuid = taskUuid
        self.folderPath = folderPath
        self.encZipPath = encZipPath
        self.passwd = passwd
        self.workingPath = workingPath
        self.syncer = collectionSync.collectionSync(taskUuid, folderPath,
                                    encZipPath, passwd, workingPath)
        #Register to folder scanner
        monitorRpcServerUrl = 'http://localhost:8806/xmlrpc'
        syncRpcServerUrl = 'http://localhost:8807/xmlrpc'
        proxy = xmlrpclib.ServerProxy(monitorRpcServerUrl)
        self.encZipPathMonitorUrl = proxy.register(self.encZipPath, syncRpcServerUrl)
        self.folderPathMonitorUrl = proxy.register(self.folderPath, syncRpcServerUrl)

        
    def subClassRun(self, notifyParam):
        cl('subClassRun called', notifyParam)
        self.syncer.process()
        cl('process end')


    def checkMonitorUrl(self, monitorUrl):
        if (monitorUrl == self.encZipPathMonitorUrl) or (monitorUrl == self.folderPathMonitorUrl):
            return True
        else:
            return False
class syncXmlRpcServer(xmlRpcServerWithWorkerThreadBase.xmlRpcServerWithWorkerThreadBase):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        xmlRpcServerWithWorkerThreadBase.xmlRpcServerWithWorkerThreadBase.__init__(self)
        #self.uuidDict = {}
    def addSync(self, taskUuid, folderPath, encZipPath, passwd, workingPath):
        threadInst = syncThread(taskUuid, folderPath, encZipPath, passwd, workingPath)
        self.register(taskUuid, threadInst)
        threadInst.start()
        #print self.encZipPath
        #print self.folderPath
        #print syncRpcServerUrl

    addSync.exposed = True
    
    def notify(self, notifyParam):
        for i in self.itemList:
            if self.itemList[i].checkMonitorUrl(notifyParam):
                self.itemList[i].notify(notifyParam)
    notify.exposed = True
    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerWithWorkerThreadBase.startMainServer(syncXmlRpcServer(), 8807)