from localLibs.qtconsole.CrossGuiLauncher import start_cross_gui_launcher

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



if __name__ == "__main__":
    start_cross_gui_launcher(autoStartAppList)
