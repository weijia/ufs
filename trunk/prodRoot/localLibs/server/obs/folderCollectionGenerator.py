'''
Created on 2011-9-21

@author: Richard
'''
import xmlrpclib
import os
#import cherrypy
import threading
from cherrypy import _cptools

import localLibSys
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.objectDatabaseV3 as objectDatabase
import localLibs.objSys.ufsObj as ufsObj
import xmlRpcServerBase

import xmlRpcServerWithWorkerThreadBaseV2 as xmlRpcServerWithWorkerThreadBase

class dirScanner(xmlRpcServerWithWorkerThreadBase.serverThread):
    def __init__(self, rootFolder, xmlRpcCallbackServer, targetCollectionId = None, dbPrefix = ""):
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        if not (targetCollectionId is None):
            self.targetCollectionId = targetCollectionId
        else:
            self.targetCollectionId = "folder://" + self.rootFolder
        self.objDb = objectDatabase.objectDatabase(dbPrefix = dbPrefix)
        self.addedItemCnt = 0
        #The following will call initFirstItem and initFirstItem will use 
        #self.rootFolder and self.targetCollectionId, so the following must
        #be called after all these members are initialized
        xmlRpcServerWithWorkerThreadBase.serverThread.__init__(self, self.targetCollectionId, 
                                                               xmlRpcCallbackServer)
    
    ##################################
    # The following are only for internal use, will only be called from manager server
    ##################################
    
    def subClassRun(self, paramDict):
        ###############################################
        #Scan for existing files
        ###############################################
        collection = self.objDb.getCollection(self.targetCollectionId)
        cl('start scanning')
        #for i in os.walk(self.rootFolder):
        for i in os.listdir(self.rootFolder):
            if (self.addedItemCnt % 1000) == 0:
                cl("processing item cnt:", self.addedItemCnt)
            self.addedItemCnt += 1

            fullPath = transform.transformDirToInternal(os.path.join(self.rootFolder, i))
            #print '---------------------real adding item'
            #Update the item info for the item
            ncl('before fs obj base')
            #itemUrl = ufsObj.fsObjBase(fullPath).getObjUrl()
            objInCol = fullPath.replace(self.rootFolder + "/", "");
            #print fullPath, self.rootFolder
            if objInCol.find("/") != -1:
                print objInCol
                raise "no recursive scanning support"
            ncl('before get fs obj')
            newObjUuid = self.objDb.getFsObjFromFullPath(fullPath)["uuid"]
            if newObjUuid is None:
                cl("item deleted, do not add it")
                continue
            ncl('before update obj uuid')
            '''
            collection.updateObjUuidIfNeeded(itemUrl, newObjUuid)
            '''
            if collection.isSame(objInCol, newObjUuid):
                ncl("no updates needed", objInCol, newObjUuid)
                continue
            collection.updateObjUuidRaw(objInCol, newObjUuid)
            ncl('new item added', objInCol)
                
        cl("notifying listener")
        self.notifyAll()


class collectionManagementServer(xmlRpcServerWithWorkerThreadBase.xmlRpcServerWithWorkerThreadBase):
    def register(self, monitorUrl, xmlRpcServerUrl, dbPrefix = ""):
        #paramDict = {"rootFolder": monitorUrl, "serverUrl": xmlRpcServerUrl}
        newProcessor = dirScanner(monitorUrl, xmlRpcServerUrl, dbPrefix)
        targetCallbackServerUrl = self.createProcessor(newProcessor)
        if targetCallbackServerUrl == newProcessor.getFirstCallbackServerUrl():
            newProcessor.msg("subClassRun", {})
        return newProcessor.getThreadHndl()
    register.exposed = True

if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(collectionManagementServer(8808))