from localLibs.logWin.AdvScriptRunnerWithTag import AdvScriptRunnerWithTag
from localLibs.services.beanstalkdServices.BeanstalkdLauncherService import BeanstalkdLauncherService 

autoStartAppList = ['mongodb.bat',
                    'startBeanstalkd.bat',
                    'webserver-cgi',
                    #'XmlRpcServer2BeanstalkdServiceBridge',
                    'cherrypyServerV3',
                    'BeanstalkdLauncherService',
                    'folderCollectionInitiator',
                    #'collectionMonitorNonRealtimeNotifierServiceV2',
                    #'syncXmlRpcServerV2,
                    'tubeDelayServiceV2',
                    'monitorServiceV2',
                    'folderScanner',
                    #'zippedCollectionListHandlerV2',
                    'FileArchiveServiceV2',
                    'TagProcessServiceBase'
                    ]

def main():
    r = AdvScriptRunnerWithTag()
    r.startApplicationsNoReturn(autoStartAppList, 
                                            BeanstalkdLauncherService)

if __name__ == "__main__":
    main()
