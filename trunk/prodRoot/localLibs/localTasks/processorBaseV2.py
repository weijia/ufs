import localLibs.objSys.objectDatabaseV3 as objectDatabase

class incorrectTaskAndAppId:pass

class processorBase:
    def __init__(self, taskId, appUuid):
        self.db = objectDatabase.objectDatabase()
        self.taskId = taskId
        self.appUuid = appUuid
        
    def getAppCfg(self):
        return self.db.findObj({"taskId": self.taskId, "appUuid": self.appUuid})
        
    def saveAppConfig(self):
        '''
        Do not use it externally, implement subClassInitialCfg instead
        '''
        self.appConfigObj["taskId"] = self.taskId
        self.appConfigObj["appUuid"] = self.appUuid
        '''
        res["uuid"] = unicode(str(uuid.uuid4()))
        res["taskUuid"] = res["uuid"]
        res["taskUrl"] = u"uuid://"+res["taskUuid"]
        '''
        self.appConfigObj["uuid"] = self.db.addVirtualObj(self.appConfigObj)


        
    def isAppConfigOk(self):
        if not self.checkParamInternal(self.expectedAppConfig):
            raise incorrectTaskAndAppId
        
    def checkParamInternal(self, expectedDict):
        for i in expectedDict:
            if not self.appConfigObj.has_key(i):
                return False
            if self.appConfigObj[i] != expectedDict[i]:
                return False
        return True
    