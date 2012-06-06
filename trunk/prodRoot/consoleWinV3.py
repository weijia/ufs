from localLibs.logWin.LauncherMain import LauncherMain
from localLibs.logWin.TagDropHandler import TagDropHandler
#from localLibs.services.beanstalkdServices.BeanstalkdLauncherService import BeanstalkdLauncherService 

autoStartAppList = [#'mongodb.bat',
                    #'startBeanstalkd.bat',
                    #'BeanstalkdLauncherService',
                    'webserver-cgi',
                    'cherrypyServerV4',
                    'folderCollectionInitiator',
                    'tubeDelayServiceV3',
                    'monitorServiceV2',
                    #'FolderScannerV2',#Scan folder service
                    #'FileArchiveServiceV2',#Archive info for files from input tube
                    #'UpdateCheckingService',#Check file updates and send to tube
                    #############################
                    #'AutoExtractInfoWithThumbService',
                    
                    #'ReqDumpService',
                    #'TagProcessServiceClientV2',
                    #'FolderInfoArchiveService',#Archive file info in folders from input tube 
                    #####################
                    'TagProcessServiceV2',#Process tags and do operations
                    'FolderEnumeratingService',#Enumerate folders and sub-folders
                    'FolderArchiveService',#Archive folders from input tube 
                    'AutoArchiveService',#This is a quick add service for automatically archive files
                    
                    ]


def main():
    r = LauncherMain()
    d = TagDropHandler()
    r.start_services(autoStartAppList)
    r.register_drop_handler(d)
    r.start_gui_msg_loop()

if __name__ == "__main__":
    main()
