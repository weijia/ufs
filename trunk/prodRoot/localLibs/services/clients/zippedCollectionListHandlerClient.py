'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
import localLibs.services.folderScanner as folderScanner
import localLibs.services.monitorServiceV2 as monitorService
from localLibs.services.tubeDelayServiceV2 import tubeDelayService
from localLibs.services.zippedCollectionListHandlerV2 import zippedCollectionListService


'''
fileScanner -> collectionListTube+taskUuid
monitorServiceV2 -> collectionListTube+taskUuid


collectionListTube+taskid -> delayedCollectionListTubeName+taskUuid

delayedCollectionListTubeName+taskUuid -> fileArchiveService
'''


def autoArchive(fullPath = gAutoArchiveFullPath, workingDir = gWorkingDir,taskUuid = uuid.uuid4()):
    inputTubeName = "collectionListTube"+taskUuid
    delayedCollectionListTubeName = "delayedCollectionListTubeName"+taskUuid
    
    s = folderScanner.folderScanner()
    s.addItem({"command": "folderScanner", "fullPath":"d:/tmp/generating",
               "targetTubeName": zippedListTubeName,"blackList":[]})

    s = monitorService.monitorService()
    s.addItem({"command": "folderScanner", "fullPath":"d:/tmp/generating",
               "targetTubeName": zippedListTubeName,"blackList":[]})
    
    s = tubeDelayService()
    s.addItem({"inputTubeName":zippedListTubeName,
               "outputTubeName": delayedZippedInfoListTubeName,"blackList":[]})
    
    s = zippedCollectionListService()
    s.addItem({"inputTubeName":delayedZippedInfoListTubeName})