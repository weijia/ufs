'''
Created on 2011-9-22

@author: Richard
'''
import os
import xmlrpclib


import localLibSys
from localLibs.logSys.logSys import *
import xmlRpcServerBase
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.objectDatabaseV3 as objectDatabase

gXmlRpcServerPort = 9907
gXmlRpcServerUrl = u"http://127.0.0.1:%d/xmlrpc"%gXmlRpcServerPort


import wwjufsdatabase.libs.services.servicesV2 as service

import xmlRpcServerWithThread as threadSvrBase

class workThread(threadSvrBase.serverThread):
    def __init__(self, outputFolder, rootFolder, username = "system.demoUser", passwd = "nopass", targetCollectionId = None
                 , dbPrefix = "test"):
        #print rootFolder
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        self.outputFolder = transform.transformDirToInternal(outputFolder)
        #print self.rootFolder
        threadHndl = "recursive://" + self.rootFolder
        self.userSession = service.ufsUser(username, passwd)
        #print username, passwd
        self.objDb = objectDatabase.objectDatabase(self.userSession, dbPrefix = dbPrefix)
#        if not (targetCollectionId is None):
#            self.targetCollectionId = targetCollectionId
#        else:
#            self.targetCollectionId = "folder://" + self.rootFolder
        super(workThread, self).__init__(threadHndl, "singleton")
#        self.partialRes = []
        self.addedItemCnt = 0
        
        
    ##################################
    # The following are only for internal use, will only be called from 
    # this class itself, calling these methods by sending message 
    # to this class with no "Internal"
    ##################################
    def genInternal(self, param):
        proxy = xmlrpclib.ServerProxy("http://localhost:9906/xmlrpc")
        #argv1 task id, argv2 passwd
        targetUrl = proxy.create(self.rootFolder, 1, "system.demoUser", "nopass", "http://localhost:9907/xmlrpc")
        cl(targetUrl)


class folderInfoStorageServer(threadSvrBase.xmlRpcServerWithThread):
    '''
    classdocs
    '''
    def __init__(self, port):
        '''
        Constructor
        '''
        super(folderInfoStorageServer, self).__init__(port)
        
    def create(self, outputFolder, rootPath):
        threadInst = workThread(outputFolder, rootPath)
        clientId = self.createProcessor(threadInst)
        ncl(clientId)
        threadInst.msg("gen", {})
        return "OK"
    create.exposed = True
    
    def notify(self, param):
        cl(param)
        threadInst = self.getThreadInst(param.replace("folder://", "recursive://"))
        threadInst.msg("scanComplete", {})
        
    notify.exposed = True
    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(folderInfoStorageServer(gXmlRpcServerPort))