from localLibs.logWin.LauncherMain import LauncherMain
from localLibs.logWin.TagDropHandler import TagDropHandler
#from localLibs.services.beanstalkdServices.BeanstalkdLauncherService import BeanstalkdLauncherService 

autoStartAppList = ['mongodb.bat',
                    #'startBeanstalkd.bat',
                    'webserver-cgi',
                    #'XmlRpcServer2BeanstalkdServiceBridge',
                    'cherrypyServerV3',
                    #'BeanstalkdLauncherService',
                    'folderCollectionInitiator',
                    #'collectionMonitorNonRealtimeNotifierServiceV2',
                    #'syncXmlRpcServerV2,
                    'tubeDelayServiceV3',
                    'monitorServiceV2',
                    'folderScanner',
                    #'zippedCollectionListHandlerV2',
                    'FileArchiveServiceV2',
                    'TagProcessServiceBase'
                    ]


def main():
    r = LauncherMain()
    d = TagDropHandler()
    r.start_services(autoStartAppList)
    r.register_drop_handler(d)
    r.start_gui_msg_loop()

if __name__ == "__main__":
    main()