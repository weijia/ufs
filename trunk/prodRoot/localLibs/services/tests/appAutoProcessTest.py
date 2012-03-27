'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
import localLibs.services.folderScanner as folderScanner
import localLibs.services.monitorServiceV2 as monitorService
from localLibs.services.tubeDelayServiceV2 import tubeDelayService
from localLibs.services.zippedCollectionListHandlerV2 import zippedCollectionListService
from localLibs.services.autoProcessService import autoProcessService
'''
fileScanner->fileListTube
monitorServiceV2->fileListTube
'''


gMonitoringPath = "D:\\codes\\nsn\\lte\\ueSim\\latest-uesim-codes"
gWorkingDir = "D:/tmp/working/autoProcessWorkingDir"


def autoProcess(workingDir = gWorkingDir,fullPath = gMonitoringPath):
    inputTubeName = "collectionListTubeForAutoProcess"
    delayedCollectionListTubeName = "delayedCollectionListTubeNameForAutoProcess"
    '''
    s1 = folderScanner.folderScanner()
    s1.addItem({"command": "folderScanner", "fullPath":fullPath,
               "targetTubeName": inputTubeName,"blackList":[]})
    '''
    s2 = monitorService.monitorService()
    s2.addItem({"command": "monitorService", "fullPath":fullPath,
               "targetTubeName": inputTubeName,"blackList":[]})
    
    s3 = tubeDelayService()
    s3.addItem({"inputTubeName":inputTubeName,
               "outputTubeName": delayedCollectionListTubeName,
               "delaySeconds": 15,
               "blackList":[]})
    
    s4 = autoProcessService()
    s4.addItem({"inputTubeName":delayedCollectionListTubeName, "appsList":workingDir})
    
    
if __name__ == "__main__":
    autoProcess()