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
        self.archivePendingCollectionId = self.appConfigObj["archivePendingCollectionId"]
        self.extractionPendingCollectionId = self.appConfigObj["extractionPendingCollectionId"]
        self.archivePending = collectionDatabase.collectionOnMongoDbBase(self.archivePendingCollectionId, 
                                                                            collectionDbInst)
        self.extractionPending = collectionDatabase.collectionOnMongoDbBase(self.extractionPendingCollectionId, 
                                                                            collectionDbInst)
        
        self.lastTimestamp = self.appConfigObj["nextToProcessTimestamp"]
    
    ##################################
    # The following functions are standard processor methods
    ##################################
    def subClassInitialCfg(self):
        return {"archivePendingCollectionId": unicode(str(uuid.uuid4())), 
                "extractionPendingCollectionId": unicode(str(uuid.uuid4())), 
                "srcCollectionId": self.srcCollectionId,
                "destCollectionId":self.destCollectionId}
        
    def process(self):
        while True:
            self.syncCollection()
            break
            
    ##################################
    # The following functions are for internal use
    ##################################

    def syncCollection(self):
        ##############################
        #Calling interface function enumObjWithPendingCollection
        ##############################
        for obj, curTimestamp in self.srcCollection.subClassEnumWithPending(self.appConfigObj["nextToProcessTimestamp"], self.pendingCollection):
            ncl(obj, curTimestamp)
            srcObjUuid = self.srcCollection.getObjUuid(obj["idInCol"])
            #ncl(self.destCollection.getObjUuid(obj["idInCol"]))
            storeFlag = True
            if self.destCollection.exists(obj["idInCol"]):
                cl('exists in dest collection')
                #Already there, check if it was updated
                dstObjUuid = self.destCollection.getObjUuid(obj["idInCol"])
                ncl('dest uuid:', dstObjUuid)
                if not self.db.isUpdated(srcObjUuid, dstObjUuid):
                    cl("item not updated, ignore")
                    storeFlag = False
            if storeFlag:
                ncl('store file')
                self.destCollection.store(obj, self.pendingCollection)
                ##############################
                #Calling interface function enumObjWithPendingCollection
                ##############################
                #No need to call this? It is not needed for extraction
                #And it is not needed for archiver either
                #self.srcCollection.complete(obj, self.pendingCollection)
            ncl('before update uuid')
            self.db.updateObjByUuid(self.appConfigObj["uuid"], {"nextToProcessTimestamp": curTimestamp})
            ncl('update task info completed', "nextToProcessTimestamp:", curTimestamp)
        self.destCollection.enumEnd(self.pendingCollection)

            
class encZipProcessor(advCollectionProcessor):
    def __init__(self, taskId, appUuid, targetRootDir, targetBackupDir, 
                            collectionId, workingDir, passwd):
                            
        #First set the input param, __init__ will create initial config from this by calling subClassInitialCfg
        advCollectionProcessor.__init__(self, taskId, appUuid, collectionId)
        #The param initiated in this class should be check by this class
        if self.appConfigObj["logCollectionId"] != logCollectionId:
            raise "Task parameter does not match"

        #Create the 2 collections
        #print self.db
        self.folderCol = syncFolderCollection.syncFolderCollection(transform.transformDirToInternal(targetRootDir), 
                                transform.transformDirToInternal(targetBackupDir),
                                syncFolderCollectionId, self.db)
        self.encZipCol = encZipCollection.encZipCollection(transform.transformDirToInternal(collectionId), 
                                logCollectionId, 
                                transform.transformDirToInternal(workingDir), passwd, self.db)
        
    def subClassInitialCfg(self):
        param = advCollectionProcessor.subClassInitialCfg(self)
        param["logCollectionId"] = unicode(str(uuid.uuid4()))
        return param
    def process(self):
        while True:
            self.archiveFlag = False
            self.updateCollection()
            self.archiveFlag = True
            self.updateCollection()
            break
            
    def updateCollection(self):
        if self.archiveFlag:
            self.srcCollection =  self.folderCol
            self.destCollection = self.encZipCol
            self.pendingCollection = self.archivePending
        else:
            self.srcCollection =  self.encZipCol
            self.destCollection = self.folderCol
            self.pendingCollection = self.extractionPending
        self.syncCollection()
        
gAppUuid = 'fa38c942-15ed-4fa8-a0d2-a7ab013e5c0b'
            
            
            
def main():
    import sys
    #print sys.argv[1]
    suffix = '3i'
    syncFolderCollectionId = 'uuid://088b222c-d86c-4a59-8084-3cfc9aa3fcce' + suffix
    logCollectionId = 'uuid://c6e1e1a8-8e18-42d5-b1e1-0a249380494' + suffix
    taskName = "test task10" + suffix
    s = encZipProcessor(taskName, gAppUuid, "D:/tmp/fileman/target/data", "D:/tmp/fileman/target/backup",
                                syncFolderCollectionId,
                                transform.transformDirToInternal("D:\\tmp\\fileman\\data\\encZip"), 
                                logCollectionId, "D:/tmp/dbOrientTest", sys.argv[1])
    s.process()
    
     
if __name__ == '__main__':
    main()
