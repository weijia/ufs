'''
Created on 2011-9-22

@author: Richard
'''
import os


import localLibSys
from localLibs.logSys.logSys import *
import xmlRpcServerBase
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.objectDatabaseV3 as objectDatabase

gXmlRpcServerPort = 9906
gXmlRpcServerUrl = u"http://127.0.0.1:%d/xmlrpc"%gXmlRpcServerPort


import wwjufsdatabase.libs.services.servicesV2 as service

import xmlRpcNotifier as threadSvrBase

class workThread(threadSvrBase.xmlRpcNotifier):
    def __init__(self, rootFolder, username = "system.demoUser", passwd = "nopass", targetCollectionId = None
                 , dbPrefix = "test", notifyServer = None):
        #print rootFolder
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        #print self.rootFolder
        threadHndl = "folder://" + self.rootFolder
        self.userSession = service.ufsUser(username, passwd)
        print username, passwd
        self.objDb = objectDatabase.objectDatabase(self.userSession, dbPrefix = dbPrefix)
        if not (targetCollectionId is None):
            self.targetCollectionId = targetCollectionId
        else:
            self.targetCollectionId = "folder://" + self.rootFolder
        super(workThread, self).__init__(threadHndl, notifyServer)
        self.partialRes = []
        self.addedItemCnt = 0
        
    def getPartialResult(self, maxNum):
        cnt = 0
        self.gen = self.generator()
        for i in self.gen:
            self.partialRes.append(i)
            #print "got item:", i
            cnt += 1
            if cnt >= maxNum:
                return self.gen
            
    def genInternal(self, param):
        for k in self.gen:
            #print "in thread got item:", k
            continue
        self.notifyAll()
        
    def generator(self):
        ###############################################
        #Scan for existing files
        ###############################################
        collection = self.objDb.getCollection(self.targetCollectionId)
        cl('start scanning')
        #for i in os.walk(self.rootFolder):
        for i in os.listdir(self.rootFolder+ "/"):
            if (self.addedItemCnt % 1000) == 0:
                cl("processing item cnt:", self.addedItemCnt)
            self.addedItemCnt += 1

            fullPath = transform.transformDirToInternal(os.path.join(self.rootFolder, i))
            #print '---------------------real adding item'
            #Update the item info for the item
            ncl('before fs obj base')
            #itemUrl = ufsObj.fsObjBase(fullPath).getObjUrl()
            objInCol = transform.getRelativePathFromFull(fullPath, self.rootFolder)
            #print fullPath, self.rootFolder
            if objInCol.find("/") != -1:
                print objInCol, self.rootFolder
                raise "no recursive scanning support"
            ncl('before get fs obj')
            newObjUuid = self.objDb.getFsObjFromFullPath(fullPath)["uuid"]
            #print fullPath
            if newObjUuid is None:
                cl("item deleted, do not add it")
                continue
            ncl('before update obj uuid')
            '''
            collection.updateObjUuidIfNeeded(itemUrl, newObjUuid)
            '''
            if collection.isSame(objInCol, newObjUuid):
                ncl("no updates needed", objInCol, newObjUuid)
                yield objInCol
                continue
            collection.updateObjUuidRaw(objInCol, newObjUuid)
            ncl('new item added', objInCol)
            yield objInCol
        folderObj = self.objDb.getFsObjFromFullPath(self.rootFolder)
        self.objDb.updateObjByUuid(folderObj["uuid"], 
                                           {"folderCollectionId": self.targetCollectionId})
        cl(folderObj, {"folderCollectionId": self.targetCollectionId})

class folderCollectionServer(threadSvrBase.notifierServer):
    '''
    classdocs
    '''
    def __init__(self, port):
        '''
        Constructor
        '''
        super(folderCollectionServer, self).__init__(port)
        
    def create(self, rootPath, retNum, username, passwd, notifyServer):
        threadInst = workThread(rootPath, username, passwd, notifyServer = notifyServer)
        res = threadInst.getPartialResult(retNum)
        clientId = self.createProcessor(threadInst)
        ncl(clientId)
        threadInst.msg("gen", {})
        return threadInst.partialRes
    create.exposed = True
    

    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(folderCollectionServer(gXmlRpcServerPort))