'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
import localLibs.services.folderScanner as folderScanner
'''
fileScanner->fileListTube
monitorServiceV2->fileListTube
'''
if __name__ == "__main__":
    s = folderScanner.folderScanner()
    s.addItem({"command": "folderScanner", "fullPath":"d:/tmp/monitoring",
               "targetTubeName": "fileListTube","blackList":[]})