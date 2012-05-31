'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
#import localLibs.services.beanstalkdServices.FolderScannerV2 as FolderScanner
import localLibs.services.beanstalkdServices.UpdateCheckingService as UpdateCheckingService
import localLibs.services.beanstalkdServices.monitorServiceV2 as monitorService
from localLibs.services.beanstalkdServices.tubeDelayServiceV3 import tubeDelayService
#from localLibs.services.zippedCollectionListHandlerV2 import zippedCollectionListService
from localLibs.services.beanstalkdServices.FileArchiveServiceV2 import FileArchiveService
import wwjufsdatabase.libs.utils.transform as transform 

'''
fileScanner -> collectionListTube+taskUuid
monitorServiceV2 -> collectionListTube+taskUuid


collectionListTube+taskid -> delayedCollectionListTubeName+taskUuid

delayedCollectionListTubeName+taskUuid -> fileArchiveService

'''


gAutoArchiveFullPath = "D:\\userdata\\q19420\\My Documents\\Tencent Files\\10132994\\Image"
gWorkingDir = "D:/tmp/working/fileArchiveService"
g_default_target_dir = "D:/tmp/working/default_target_dir"
g_ignore_file_type_list = ["*.c", "*.h", "*.cpp","*.hpp"]
g_ignore_file_type_list = []

def AutoArchiveThumb(source_folder = gAutoArchiveFullPath, target_dir = g_default_target_dir,
                     workingDir = gWorkingDir,taskUuid = str(uuid.uuid4())):
    inputTubeName = "collectionListTube"+taskUuid
    delayedCollectionListTubeName = "delayedCollectionListTubeName"+taskUuid
    
    #s1 = FolderScanner.FolderScanner()
    #s1.addItem({"command": "folderScanner", "fullPath":source_folder,
    #           "targetTubeName": inputTubeName,"blackList":g_ignore_file_type_list})
    target_dir = transform.transformDirToInternal(target_dir)
    source_folder = transform.transformDirToInternal(source_folder)
    
    storage_state_collection_name = "storage_state://"+source_folder+":"+target_dir
    s1 = UpdateCheckingService.UpdateCheckingService()
    s1.addItem({"full_path": source_folder, "black_list":[], 
                "target_tube_name": inputTubeName, "state_collection_id": storage_state_collection_name
                })

    s2 = monitorService.monitorService()
    s2.addItem({"command": "monitorService", "fullPath":source_folder,
               "targetTubeName": inputTubeName,"blackList":g_ignore_file_type_list})
    
    s3 = tubeDelayService()
    s3.addItem({"inputTubeName":inputTubeName,
               "outputTubeName": delayedCollectionListTubeName,"blackList":g_ignore_file_type_list})
    
    s4 = FileArchiveService()
    s4.addItem({"InputTubeName":delayedCollectionListTubeName, "WorkingDir":workingDir, "TargetDir": target_dir})
    
    
if __name__ == "__main__":
    AutoArchiveThumb()