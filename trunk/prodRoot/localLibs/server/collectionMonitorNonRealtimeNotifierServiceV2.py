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
import xmlRpcServerBase

import xmlRpcServerWithWorkerThreadBaseV2 as xmlRpcServerWithWorkerThreadBase

class dirRecursiveScanner(xmlRpcServerWithWorkerThreadBase.serverThread):
    def __init__(self, rootFolder, xmlRpcCallbackServer, targetCollectionId = None, dbPrefix = ""):
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        if not (targetCollectionId is None):
            self.targetCollectionId = targetCollectionId
        else:
            self.targetCollectionId = u'folderRecursiveEnum://'+self.rootFolder
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
        for i in os.walk(self.rootFolder):
            #cl(i)
            for j in i[2]:
                if (self.addedItemCnt % 1000) == 0:
                    cl("processing item cnt:", self.addedItemCnt)
                self.addedItemCnt += 1

                fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
                #print '---------------------real adding item'
                #Update the item info for the item
                ncl('before fs obj base')
                itemUrl = objectDatabase.fsObjBase(fullPath).getObjUrl()
                ncl('before get fs obj')
                newObjUuid = self.objDb.getFsObjUuid(itemUrl)
                if newObjUuid is None:
                    cl("item deleted, do not add it")
                    continue
                ncl('before update obj uuid')
                '''
                collection.updateObjUuidIfNeeded(itemUrl, newObjUuid)
                '''
                if collection.isSame(itemUrl, newObjUuid):
                    ncl("no updates needed", itemUrl, newObjUuid)
                    continue
                collection.updateObjUuidRaw(itemUrl, newObjUuid)
                ncl('new item added', itemUrl)
                
        cl("notifying listener")
        self.notifyAll()


class collectionManagementServer(xmlRpcServerWithWorkerThreadBase.xmlRpcServerWithWorkerThreadBase):
    def register(self, monitorUrl, xmlRpcServerUrl):
        #paramDict = {"rootFolder": monitorUrl, "serverUrl": xmlRpcServerUrl}
        newProcessor = dirRecursiveScanner(monitorUrl, xmlRpcServerUrl)
        targetCallbackServerUrl = self.createProcessor(newProcessor)
        if targetCallbackServerUrl == newProcessor.getFirstCallbackServerUrl():
            newProcessor.msg("subClassRun", {})
        return newProcessor.getThreadHndl()
    register.exposed = True

if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(collectionManagementServer(8806))