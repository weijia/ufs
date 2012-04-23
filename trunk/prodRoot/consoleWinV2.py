from localLibs.logWin.AdvScriptRunnerWithTag import AdvScriptRunnerWithTag
import localLibs.logWin.advScriptRunnerXmlRpcServer as advScriptRunnerXmlRpcServer

autoStartAppList = ['mongodb.bat',
                    'startBeanstalkd.bat',
                    'webserver-cgi',
                    'XmlRpcServer2BeanstalkdServiceBridge',
                    'cherrypyServerV3',
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
                                            advScriptRunnerXmlRpcServer.launcherXmlRpcThread)

if __name__ == "__main__":
    main()
