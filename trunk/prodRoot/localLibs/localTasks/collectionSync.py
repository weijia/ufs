import uuid
import localLibSys
import localLibs.collection.syncFolderCollection as syncFolderCollection
import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import localLibs.localTasks.processorBaseV2 as processorBase
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.encZip.encZipCollectionV2 as encZipCollection
import os
from localLibs.logSys.logSys import *

gAppUuid = 'fa38c942-15ed-4fa8-a0d2-a7ab013e5c0b'

class collectionSync(processorBase.processorBase):
    def __init__(self, taskId, folderRoot, 
                            encZipRoot, passwd, workingDir = 'd:/tmp/fileman/working', appUuid = gAppUuid):
        processorBase.processorBase.__init__(self, taskId, appUuid)
        self.appConfigObj = self.getAppCfg()
        if self.appConfigObj is None:
            self.appConfigObj = {}
            self.appConfigObj["encZipRoot"] = transform.transformDirToInternal(encZipRoot)
            self.appConfigObj["folderRoot"] = transform.transformDirToInternal(folderRoot)
            self.appConfigObj["workingDir"] = transform.transformDirToInternal(workingDir)
            self.appConfigObj["targetBackupDir"] = transform.transformDirToInternal(os.path.join(workingDir, "backup"))
            self.appConfigObj["syncFolderCollectionId"] = unicode(str(uuid.uuid4()))
            self.appConfigObj["logCollectionId"] = unicode(str(uuid.uuid4()))
            self.appConfigObj["archivePendingCollectionId"] = unicode(str(uuid.uuid4()))
            self.appConfigObj["extractionPendingCollectionId"] = unicode(str(uuid.uuid4()))
            self.appConfigObj["archiveNextToProcessTimestamp"] = 0
            self.appConfigObj["extractionNextToProcessTimestamp"] = 0
            self.saveAppConfig()
        else:
            self.expectedDict = {}
            self.expectedDict["encZipRoot"] = transform.transformDirToInternal(encZipRoot)
            self.expectedDict["folderRoot"] = transform.transformDirToInternal(folderRoot)
            self.expectedDict["workingDir"] = transform.transformDirToInternal(workingDir)
            self.expectedDict["targetBackupDir"] = transform.transformDirToInternal(os.path.join(workingDir, "backup"))            
            self.checkParamInternal(self.expectedDict)
        self.curTimestampName = "extractionNextToProcessTimestamp"

        self.archivePendingCollectionId = self.appConfigObj["archivePendingCollectionId"]
        self.extractionPendingCollectionId = self.appConfigObj["extractionPendingCollectionId"]
        self.syncFolderCollectionId = self.appConfigObj["syncFolderCollectionId"]
        self.logCollectionId = self.appConfigObj["logCollectionId"]
        
        collectionDbInst = self.db.getCollectionDb()        
        self.archivePending = collectionDatabase.collectionOnMongoDbBase(self.archivePendingCollectionId, 
                                                                            collectionDbInst)
        self.extractionPending = collectionDatabase.collectionOnMongoDbBase(self.extractionPendingCollectionId, 
                                                                            collectionDbInst)
        
        #Create the 2 collections
        #print self.db
        self.folderCol = syncFolderCollection.syncFolderCollection(self.appConfigObj["folderRoot"], 
                                self.appConfigObj["targetBackupDir"],
                                self.appConfigObj["syncFolderCollectionId"], self.db)
        self.encZipCol = encZipCollection.encZipCollection(self.appConfigObj["encZipRoot"], 
                                self.appConfigObj["logCollectionId"], 
                                self.appConfigObj["workingDir"], passwd, self.db)
        ncl(self.appConfigObj)
        
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
            self.curTimestampName = "archiveNextToProcessTimestamp"
        else:
            self.srcCollection =  self.encZipCol
            self.destCollection = self.folderCol
            self.pendingCollection = self.extractionPending
            self.curTimestampName = "extractionNextToProcessTimestamp"
        self.syncCollection()


    def syncCollection(self):
        ##############################
        #Calling interface function enumObjWithPendingCollection
        ##############################
        for obj, curTimestamp in self.srcCollection.subClassEnumWithPending(self.appConfigObj[self.curTimestampName], self.pendingCollection):
            ncl(obj, curTimestamp)
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
    taskName = sys.argv[1]
    s = collectionSync(taskName, "D:\\sys\\pidgin\\profile",
                                "D:\\sys\\pidgin\\encZip", sys.argv[2])
    s.process()
    
     
if __name__ == '__main__':
    main()