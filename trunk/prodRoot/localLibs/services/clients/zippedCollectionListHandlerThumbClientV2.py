'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
import localLibs.services.beanstalkdServices.FolderScannerV2 as FolderScanner
import localLibs.services.beanstalkdServices.monitorServiceV2 as monitorService
from localLibs.services.beanstalkdServices.tubeDelayServiceV3 import tubeDelayService
#from localLibs.services.zippedCollectionListHandlerV2 import zippedCollectionListService
from localLibs.services.beanstalkdServices.FileArchiveServiceV2 import FileArchiveService
from localLibs.services.beanstalkdServices.ArchiveUploadService import ArchiveUploadService

'''
fileScanner -> collectionListTube+taskUuid
monitorServiceV2 -> collectionListTube+taskUuid


collectionListTube+taskid -> delayedCollectionListTubeName+taskUuid

delayedCollectionListTubeName+taskUuid -> fileArchiveService

'''


gAutoArchiveFullPath = "D:\\userdata\\q19420\\My Documents\\Tencent Files\\10132994\\Image"
gWorkingDir = "D:/tmp/working/fileArchiveService"
g_default_target_dir = "D:/tmp/working/default_target_dir"
g_sync_folder = "D:/sys/sync"
g_ignore_file_type_list = ["*.c", "*.h", "*.cpp","*.hpp"]
g_ignore_file_type_list = []

def AutoArchiveThumb(source_folder = gAutoArchiveFullPath, target_dir = g_default_target_dir,
                     workingDir = gWorkingDir, sync_folder = g_sync_folder, taskUuid = str(uuid.uuid4())):
    inputTubeName = "collectionListTube"+taskUuid
    delayedCollectionListTubeName = "delayedCollectionListTubeName"+taskUuid
    sync_input_tube_name = "sync_input_tube_name" + taskUuid
    
    s1 = FolderScanner.FolderScanner()
    s1.addItem({"command": "folderScanner", "fullPath":source_folder,
               "targetTubeName": inputTubeName,"blackList":g_ignore_file_type_list})

    s2 = monitorService.monitorService()
    s2.addItem({"command": "monitorService", "fullPath":source_folder,
               "targetTubeName": inputTubeName,"blackList":g_ignore_file_type_list})
    
    s3 = tubeDelayService()
    s3.addItem({"inputTubeName":inputTubeName,
               "outputTubeName": delayedCollectionListTubeName,"blackList":g_ignore_file_type_list})
    
    s4 = FileArchiveService()
    s4.addItem({"InputTubeName":delayedCollectionListTubeName, "WorkingDir":workingDir, "TargetDir": target_dir, "finalizeNotifyTubeName":sync_input_tube_name})
    
    s5 = ArchiveUploadService()
    s5.add_archive_target(sync_input_tube_name, sync_folder)
    
    
if __name__ == "__main__":
    AutoArchiveThumb()