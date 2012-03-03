'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
import localLibs.services.monitorServiceV2 as monitorService
'''
fileScanner->fileListTube
monitorServiceV2->fileListTube
'''
if __name__ == "__main__":
    s = monitorService.monitorService()
    s.addItem({"command": "folderScanner", "fullPath":"d:/tmp/monitoring",
               "targetTubeName": "fileListTube","blackList":[]})