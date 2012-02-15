import uuid
import localLibSys
import localLibs.collection.syncFolderCollection as syncFolderCollection
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import localLibs.localTasks.processorBaseV2 as processorBase
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.storage.infoStorage.encZipInfoCollection as encZipInfoCollection
import os
from localLibs.logSys.logSys import *
import localLibs.collection.objectDatabaseV2 as objectDatabase


gAppUuid = 'fa87bb0b-9d1e-4f20-bddd-8274f59a7e34'

class collectionSync(processorBase.processorBase):
    def __init__(self, taskId, collection1, 
                            collection2, appUuid = gAppUuid):
        processorBase.processorBase.__init__(self, taskId, appUuid)
        self.appConfigObj = self.getAppCfg()
        if self.appConfigObj is None:
            self.appConfigObj = {}
            self.appConfigObj["pendingCollectionId"] = unicode(str(uuid.uuid4()))
            self.appConfigObj["nextToProcessTimestamp"] = 0
            self.saveAppConfig()
        else:
            self.expectedDict = {}         
            self.checkParamInternal(self.expectedDict)
        self.curTimestampName = "extractionNextToProcessTimestamp"

        self.pendingCollectionId = self.appConfigObj["pendingCollectionId"]
        
        collectionDbInst = self.db.getCollectionDb()        
        self.pending = collectionDatabase.collectionOnMongoDbBase(self.pendingCollectionId, 
                                                                            collectionDbInst)
        #Create the 2 collections
        #print self.db
        self.folderCol = collection1
        self.encZipCol = collection2
        ncl(self.appConfigObj)
        
    def process(self):
        while True:
            self.archiveFlag = True
            self.updateCollection()
            break
            
    def updateCollection(self):
        if self.archiveFlag:
            self.srcCollection =  self.folderCol
            self.destCollection = self.encZipCol
            self.pendingCollection = self.pending
            self.curTimestampName = "nextToProcessTimestamp"
        self.syncCollection()


    def syncCollection(self):
        ##############################
        #Calling interface function enumObjWithPendingCollection
        ##############################
        for obj, curTimestamp in self.srcCollection.subClassEnumWithPending(self.appConfigObj[self.curTimestampName], self.pendingCollection):
            cl(obj, curTimestamp)
            srcObjUuid = self.srcCollection.getObjUuid(obj["idInCol"])
            #ncl(self.destCollection.getObjUuid(obj["idInCol"]))
            storeFlag = True
            if self.destCollection.exists(obj["idInCol"]):
                cl('exists in dest collection')
                #Already there, check if it was updated
                dstObjUuid = self.destCollection.getObjUuid(obj["idInCol"])
                ncl('dest uuid:', dstObjUuid, 'src:', srcObjUuid)
                if not self.db.isUpdated(srcObjUuid, dstObjUuid):
                    cl("item not updated, ignore", obj["idInCol"])
                    storeFlag = False
                    ############################
                    # Remove the item from pending collection!!!
                    self.pendingCollection.remove(obj["idInCol"])
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
            self.db.updateObjByUuid(self.appConfigObj["uuid"], {self.curTimestampName: curTimestamp})
            #Update the internal timestamp so the next enumerate will start at the correct position
            #even this object is not re-constructed
            self.appConfigObj[self.curTimestampName] = curTimestamp
            ncl('update task info completed', self.curTimestampName, curTimestamp)
        self.destCollection.enumEnd(self.pendingCollection)
        
def main():
    import sys
    #print sys.argv[1]
    taskName = sys.argv[2]
    
    passwd = sys.argv[1]
    db = objectDatabase.objectDatabase(dbPrefix = "test")
    folderRoot = transform.transformDirToInternal("D:\\proj")
    workingDir = 'd:/tmp/fileman/working'
    targetBackupDir = transform.transformDirToInternal(os.path.join(workingDir, "backup"))
    syncFolderCollectionId = unicode(str(uuid.uuid4()))
    
    encZipRoot = transform.transformDirToInternal("D:\\working\\test\\encZip")
    folderCol = syncFolderCollection.syncFolderCollection(folderRoot, 
                                targetBackupDir, syncFolderCollectionId, db)
    logCollectionId = unicode(str(uuid.uuid4()))
    encZipCol = encZipInfoCollection.encZipInfoCollection(encZipRoot, 
                                logCollectionId, workingDir, passwd, db)
    s = collectionSync(taskName, folderCol, encZipCol, )
    s.process()
    
     
if __name__ == '__main__':
    main()