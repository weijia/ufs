import localLibSys
import localLibs.collection.objectDatabaseV2 as objectDatabase
import uuid
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
from localLibs.logSys.logSys import *



class incorrectTaskAndAppId:pass

class processorBase:
    def __init__(self, taskId, appUuid):
        self.db = objectDatabase.objectDatabase()
        self.taskId = taskId
        self.appUuid = appUuid
        self.appConfigObj = self.db.findObj({"taskId": taskId, "appUuid":appUuid})
        if self.appConfigObj is None:
            #Task not exist, create it
            self.appConfigObj = self.getInitialCfg()
            self.appConfigObj["uuid"] = self.db.addVirtualObj(self.appConfigObj)
        if self.checkParam():
            raise incorrectTaskAndAppId()
        
        
    def getInitialCfg(self):
        '''
        Do not use it externally, implement subClassInitialCfg instead
        '''
        res = self.subClassInitialCfg()
        res["taskId"] = self.taskId
        res["appUuid"] = self.appUuid
        '''
        res["uuid"] = unicode(str(uuid.uuid4()))
        res["taskUuid"] = res["uuid"]
        res["taskUrl"] = u"uuid://"+res["taskUuid"]
        '''
        return res
    
    def subClassInitialCfg(self):
        '''
        Used by sub class to create config for itself.
        '''
        return {}
        
    def checkParam(self):
        return self.checkParamInternal(self.expectedAppConfig)
        
    def checkParamInternal(self, expectedDict):
        for i in expectedDict:
            if not self.appConfigObj.has_key(i):
                return False
            if self.appConfigObj[i] != expectedDict[i]:
                return False
        return True
    
class collectionProcessorBase(processorBase):
    def __init__(self, taskId, appUuid, collectionId):
        processorBase.__init__(self, taskId, appUuid)
        self.collectionId = collectionId
        self.nextToProcessTimeStamp = self.appConfigObj["nextToProcessTimestamp"]
        
    def getInitialCfg(self):
        res = processorBase.getInitialCfg(self)
        res["nextToProcessTimestamp"] = 0
        return res

class cacheCollectionProcessorBase(collectionProcessorBase):
    def __init__(self, taskId, appUuid, collectionId):
        collectionProcessorBase.__init__(self, taskId, appUuid, collectionId)
        collectionDbInst = self.db.getCollectionDb()
        #originalCollection = self.db.getFsCollection()
        self.collection = collectionDatabase.collectionOnMongoDbBase(collectionId, collectionDbInst)
        cl(collectionId)

    def afterProcess(self, curItem):
        #Update cursor in database to indicate that the encZip file was processed
        self.db.updateObjByUuid(self.appConfigObj["uuid"], {"nextToProcessTimestamp": curItem["timestamp"]})
        
    def process(self):
        while True:
            #Get an element from database
            for curItem in self.collection.enumCollectionItem(self.nextToProcessTimeStamp):
                ncl(curItem)
                curObj = self.db.getObjFromUuid(curItem["uuid"])
                cl(curObj)
                self.processItem(curObj)
                self.afterProcess(curItem)
            break
    def subClassProcessItem(self, nextObj):
        ############
        #If the object is not processed push it back by refresh its timestamp?
        ############
        self.collection.updateTimestampFromUuid(nextObj["uuid"])
    def processItem(self, nextObj):
        ncl(nextObj)
        self.subClassProcessItem(nextObj)
    '''
    def updateCacheCollectionProcessorCurObjTimestamp(self, nextObj):
    '''
    