import uuid
import localLibSys
import localLibs.collection.syncFolderCollection as syncFolderCollection
import localLibs.encZip.encZipCollectionV2 as encZipCollection
import localLibs.localTasks.processorBase as processorBase
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.collection.objectDatabaseV2 as objectDatabase



class advCollectionProcessor(processorBase.collectionProcessorBase):
    def __init__(self, taskId, appUuid, srcCollectionId, destCollectionId):
        self.srcCollectionId = srcCollectionId
        self.destCollectionId = destCollectionId
        processorBase.collectionProcessorBase.__init__(self, taskId, appUuid, srcCollectionId)
        if (self.srcCollectionId != self.appConfigObj["srcCollectionId"]) or (self.destCollectionId != 
                    self.appConfigObj["destCollectionId"]):
            cl(self.srcCollectionId, self.appConfigObj["srcCollectionId"], 
                    self.destCollectionId, self.appConfigObj["destCollectionId"])
            raise "Task parameter does not match"
        collectionDbInst = self.db.getCollectionDb()
        self.pendingCollectionId = self.appConfigObj["pendingCollectionId"]
        self.pendingCollection = collectionDatabase.collectionOnMongoDbBase(self.pendingCollectionId, 
                                                                            collectionDbInst)
        self.lastTimestamp = self.appConfigObj["nextToProcessTimestamp"]
    
    ##################################
    # The following functions are standard processor methods
    ##################################
    def subClassInitialCfg(self):
        return {"pendingCollectionId": unicode(str(uuid.uuid4())), 
                "srcCollectionId": self.srcCollectionId,
                "destCollectionId":self.destCollectionId}
        
    def process(self):
        while True:
            self.syncCollection()
            break
            
    ##################################
    # The following functions are for internal use
    ##################################
    def updatecurTimestamp(self, curTimestamp):
        if self.lastTimestamp != curTimestamp:
            self.db.updateObjByUuid(self.appConfigObj["uuid"], {"nextToProcessTimestamp": curTimestamp})
            self.lastTimestamp = curTimestamp
        
    def syncCollection(self):
        ##############################
        #Calling interface function enumObjWithPendingCollection
        ##############################
        for obj, curTimestamp in self.srcCollection.enumObjWithPendingCollection(self.appConfigObj["nextToProcessTimestamp"], self.pendingCollection):
            #ncl(obj["idInCol"])
            srcObjUuid = self.srcCollection.getObjUuid(obj["idInCol"])
            #ncl(self.destCollection.getObjUuid(obj["idInCol"]))
            if self.destCollection.exists(obj["idInCol"]):
                #Already there, check if it was updated
                dstObjUuid = self.destCollection.getObjUuid(obj["idInCol"])
                cl('dest uuid:', dstObjUuid)
                if not self.db.isUpdated(srcObjUuid, dstObjUuid):
                    cl("item not updated, ignore")
                    ##############################
                    #Calling interface function enumObjWithPendingCollection
                    ##############################
                    self.srcCollection.complete(obj, self.pendingCollection)
            
            ##############################
            #Calling interface function enumObjWithPendingCollection
            ##############################
            if self.destCollection.store(obj, self.pendingCollection):
                #If the store function return False, add the item to pendingList
                ##############################
                #Calling interface function enumObjWithPendingCollection
                ##############################
                self.srcCollection.complete(obj, self.pendingCollection)
                self.db.updateObjByUuid(self.appConfigObj["uuid"], {"nextToProcessTimestamp": curTimestamp})
                
    '''
    def addToPending(self, idInCol, objUuid):
        if self.pendingCollection.exists():
            if self.srcCollection.getObjUuid(i["idInCol"]) == objUuid:
                #Not updated, ignore the adding operation
                return
        self.pendingCollection.updateObjUuid(idInCol, objUuid)
        
    def removeFromPending(self, idInCol):
        if not self.pendingCollection.exists():
            cl(idInCol)
            raise 'Removing item not exists'
        self.pendingCollection.remove(idInCol)
    '''
            
class encZipExtractProcessor(advCollectionProcessor):
    def __init__(self, taskId, appUuid, targetRootDir, targetBackupDir, syncFolderCollectionId, 
                            collectionId, logCollectionId, workingDir, passwd):
                            
        #First set the input param, __init__ will create initial config from this by calling subClassInitialCfg
        self.logCollectionId = logCollectionId
        advCollectionProcessor.__init__(self, taskId, appUuid, collectionId, syncFolderCollectionId)
        #The param initiated in this class should be check by this class
        if self.appConfigObj["logCollectionId"] != logCollectionId:
            raise "Task parameter does not match"

        #Create the 2 collections
        #print self.db
        self.destCollection = syncFolderCollection.syncFolderCollection(transform.transformDirToInternal(targetRootDir), 
                                transform.transformDirToInternal(targetBackupDir),
                                syncFolderCollectionId, self.db)
        self.srcCollection = encZipCollection.encZipCollection(transform.transformDirToInternal(collectionId), 
                                logCollectionId, 
                                transform.transformDirToInternal(workingDir), passwd, self.db)
        
    def subClassInitialCfg(self):
        param = advCollectionProcessor.subClassInitialCfg(self)
        param["logCollectionId"] = self.logCollectionId
        return param
            
gAppUuid = 'fa38c942-15ed-4fa8-a0d2-a7ab013e5c0b'
            
            
            
def main():
    import sys
    #print sys.argv[1]
    syncFolderCollectionId = 'uuid://088b222c-d86c-4a59-8084-3cfc9aa3fcc5'
    logCollectionId = 'uuid://c6e1e1a8-8e18-42d5-b1e1-0a24938048bb'
    taskName = "test taskk6"
    s = encZipExtractProcessor(taskName, gAppUuid, "D:/tmp/fileman/target/data", "D:/tmp/fileman/target/backup",
                                syncFolderCollectionId,
                                transform.transformDirToInternal("D:\\tmp\\fileman\\data\\encZip"), 
                                logCollectionId, "D:/tmp/dbOrientTest", sys.argv[1])
    s.process()
    
     
if __name__ == '__main__':
    main()
