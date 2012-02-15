'''
Created on 2011-9-23

@author: Richard
'''
#import threading
import xmlrpclib
import localLibSys
import xmlRpcServerWithWorkerThreadBaseV2 as xmlRpcServerWithWorkerThreadBase
import localLibs.localTasks.collectionSync as collectionSync
from localLibs.logSys.logSys import *
import xmlRpcServerBase


gMonitorRpcServerUrl = 'http://localhost:8806/xmlrpc'
gSyncRpcServerUrl = 'http://localhost:8807/xmlrpc'

class syncThread(xmlRpcServerWithWorkerThreadBase.serverThread):
    def __init__(self, taskUuid, folderPath, encZipPath, passwd, workingPath):
        self.taskUuid = taskUuid
        self.folderPath = folderPath
        self.encZipPath = encZipPath
        self.passwd = passwd
        self.workingPath = workingPath
        self.syncer = collectionSync.collectionSync(taskUuid, folderPath,
                                    encZipPath, passwd, workingPath)
        #Register to folder scanner

        proxy = xmlrpclib.ServerProxy(gMonitorRpcServerUrl)
        self.encZipPathMonitorUrl = proxy.register(self.encZipPath, gSyncRpcServerUrl)
        self.folderPathMonitorUrl = proxy.register(self.folderPath, gSyncRpcServerUrl)
        xmlRpcServerWithWorkerThreadBase.serverThread.__init__(self)

        
    def subClassRun(self, paramDict):
        threadHandle = paramDict["notificationSource"]
        cl('subClassRun called', threadHandle)
        self.syncer.process()
        proxy = xmlrpclib.ServerProxy(gMonitorRpcServerUrl)
        if True:#try:
            print proxy.complete(threadHandle, gSyncRpcServerUrl)
            cl("notify the complete operation")
        else:#except:
            cl('notify with exception')
            pass
        cl('process end')

    '''
    def checkMonitorUrl(self, monitorUrl):
        if (monitorUrl == self.encZipPathMonitorUrl) or (monitorUrl == self.folderPathMonitorUrl):
            return True
        else:
            return False
    '''
    def getNotificationHandler(self):
        return (self.encZipPathMonitorUrl, self.folderPathMonitorUrl)

class syncXmlRpcServer(xmlRpcServerWithWorkerThreadBase.xmlRpcServerWithWorkerThreadBase):
    def __init__(self, port):
        '''
        Constructor
        '''
        xmlRpcServerWithWorkerThreadBase.xmlRpcServerWithWorkerThreadBase.__init__(self, port)
        self.threadList = list()

    
    #Create a sync service
    def addSync(self, taskUuid, folderPath, encZipPath, passwd, workingPath):
        threadInst = syncThread(taskUuid, folderPath, encZipPath, passwd, workingPath)
        self.createProcessor(threadInst)
        
        #Add additional notify info so the notification from dir scanner 
        #will be dispatched to specific thread
        encZipPathMonitorUrl, folderPathMonitorUrl = threadInst.getNotificationHandler()
        self.threadList.append((encZipPathMonitorUrl, folderPathMonitorUrl, threadInst))

    addSync.exposed = True
    
    def notify(self, notifyParam):
        cl("notify called", notifyParam)
        for i in self.threadList:
            if (i[0] == notifyParam) or (i[1] == notifyParam):
                i[2].msg("subClassRun", {"notificationSource": notifyParam})
    notify.exposed = True
    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(syncXmlRpcServer(8807))