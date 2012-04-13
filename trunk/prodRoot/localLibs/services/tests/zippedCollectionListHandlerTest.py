'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
from localLibs.services.clients.zippedCollectionListHandlerClient import 

'''
fileScanner->fileListTube
monitorServiceV2->fileListTube
'''
zippedListTubeName = "zippedListTube"
delayedZippedInfoListTubeName = "delayedZippedInfoListTube"

if __name__ == "__main__":
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