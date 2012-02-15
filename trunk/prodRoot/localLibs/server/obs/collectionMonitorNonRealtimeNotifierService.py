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
import localLibs.collection.objectDatabaseV2 as objectDatabase

import xmlRpcServerWithWorkerThreadBase as xmlRpcServerWithWorkerThreadBase

class dirRecursiveScanner(threading.Thread):
    def __init__(self, rootFolder, receiver, targetCollectionId = None):
        threading.Thread.__init__(self)
        self.rootFolder = transform.transformDirToInternal(rootFolder)
        self.objDb = objectDatabase.objectDatabase()
        self.receiver = receiver
        if targetCollectionId is None:
            self.targetCollectionId = u'folderRecursiveEnum://'+self.rootFolder
        else:
            self.targetCollectionId = targetCollectionId
        self.addedItemCnt = 0
    def getTargetCollectionId(self):
        return self.targetCollectionId
    
    def run(self):
        ###############################################
        #Scan for existing files
        ###############################################
        collection = self.objDb.getCollection(self.targetCollectionId)
        cl('start scanning')
        for i in os.walk(self.rootFolder):
            #cl(i)
            for j in i[2]:
                if (self.addedItemCnt % 100) == 0:
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
                

        self.receiver.sendNotification(self.targetCollectionId)
    
#class collectionScanner(object): pass

class notificationReceiver(object):
    def __init__(self, serverUrl = "http://localhost:8806/xmlrpc"):
        self.serverUrl = serverUrl
    def sendNotification(self, param):
        proxy = xmlrpclib.ServerProxy(self.serverUrl)
        try:
            print proxy.notify(param)
        except:
            pass
        
class monitoringItem(object):
    def __init__(self, monitorUrl, xmlRpcServerUrl):
        object.__init__(self)
        self.serverUrl = xmlRpcServerUrl
        self.receiver = notificationReceiver(xmlRpcServerUrl)
        self.scanner = self.getScanner(monitorUrl, self.receiver)
        self.monitorUrl = self.scanner.getTargetCollectionId()
        self.scanning = False
        self.originalMonitorUrl = monitorUrl
    def getNotifyUrl(self):
        return self.receiver.serverUrl
    def startScan(self):
        self.scanning = True
        self.scanner.start()
    def getMonitorUrl(self):
        return self.monitorUrl
    def getScanner(self, monitorUrl, receiver):
        return dirRecursiveScanner(monitorUrl, receiver)
    
class collectionMonitorNonRealtimeNotifierService(_cptools.XMLRPCController):
    '''
    This service will not issue notification (received from folder monitor) to the registered 
    task only when folder scan completes.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.monitoring = {}

    def register(self, monitorUrl, xmlRpcServerUrl):
        '''
        currently monitorUrl is not a real URL but a full path.
        '''
        cl(monitorUrl)
        #Create scanner task
        item = monitoringItem(monitorUrl, xmlRpcServerUrl)
        #Format the monitor url
        monitorUrl = item.getMonitorUrl()
        #monitorUrl = transform.transformDirToInternal(monitorUrl)
        if self.monitoring.has_key(monitorUrl):
            for i in self.monitoring[monitorUrl]:
                if xmlRpcServerUrl == i.getNotifyUrl():
                    cl("Already registered")
                    return monitorUrl
                else:
                    cl(xmlRpcServerUrl, i.getNotifyUrl())
                    self.monitoring[monitorUrl].append(item)
                    cl("New listener")
                    item.startScan()
                    return monitorUrl
        else:
            self.monitoring[monitorUrl] = [item]
            cl("New folder")
            item.startScan()
            return monitorUrl
    register.exposed = True
    

if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerWithWorkerThreadBase.startMainServer(collectionMonitorNonRealtimeNotifierService(), 8806)