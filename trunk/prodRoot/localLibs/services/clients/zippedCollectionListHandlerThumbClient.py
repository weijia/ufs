'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
import localLibs.services.folderScanner as folderScanner
import localLibs.services.monitorServiceV2 as monitorService
from localLibs.services.tubeDelayServiceV2 import tubeDelayService
#from localLibs.services.zippedCollectionListHandlerV2 import zippedCollectionListService
from localLibs.services.fileArchiveService import fileArchiveService

'''
fileScanner -> collectionListTube+taskUuid
monitorServiceV2 -> collectionListTube+taskUuid


collectionListTube+taskid -> delayedCollectionListTubeName+taskUuid

delayedCollectionListTubeName+taskUuid -> fileArchiveService

'''


gAutoArchiveFullPath = "D:\\userdata\\q19420\\My Documents\\Tencent Files\\10132994\\Image"
gWorkingDir = "D:/tmp/working/fileArchiveService"


def autoArchiveThumb(fullPath = gAutoArchiveFullPath, workingDir = gWorkingDir,taskUuid = uuid.uuid4()):
    inputTubeName = "collectionListTube"+taskUuid
    delayedCollectionListTubeName = "delayedCollectionListTubeName"+taskUuid
    
    s1 = folderScanner.folderScanner()
    s1.addItem({"command": "folderScanner", "fullPath":fullPath,
               "targetTubeName": inputTubeName,"blackList":[]})

    s2 = monitorService.monitorService()
    s2.addItem({"command": "monitorService", "fullPath":fullPath,
               "targetTubeName": inputTubeName,"blackList":[]})
    
    s3 = tubeDelayService()
    s3.addItem({"inputTubeName":inputTubeName,
               "outputTubeName": delayedCollectionListTubeName,"blackList":[]})
    
    s4 = fileArchiveService()
    s4.addItem({"inputTubeName":delayedCollectionListTubeName, "workingDir":workingDir})
    
    
if __name__ == "__main__":
    autoArchiveThumb()