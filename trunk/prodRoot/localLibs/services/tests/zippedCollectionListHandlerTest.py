'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
import localLibs.services.folderScanner as folderScanner
import localLibs.services.monitorServiceV2 as monitorService
'''
fileScanner->fileListTube
monitorServiceV2->fileListTube
'''
zippedListTubeName = "zippedListTube"

if __name__ == "__main__":
    s = folderScanner.folderScanner()
    s.addItem({"command": "folderScanner", "fullPath":"d:/tmp/target",
               "targetTubeName": zippedListTubeName,"blackList":[]})

    s = monitorService.monitorService()
    s.addItem({"command": "folderScanner", "fullPath":"d:/tmp/target",
               "targetTubeName": zippedListTubeName,"blackList":[]})