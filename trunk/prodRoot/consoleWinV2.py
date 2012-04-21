from localLibs.logWin.AdvScriptRunnerWithTag import AdvScriptRunnerWithTag
import localLibs.logWin.advScriptRunnerXmlRpcServer as advScriptRunnerXmlRpcServer

autoStartAppList = ['mongodb.bat',
                    'webserver-cgi',
                    'cherrypyServerV3',
                    'startBeanstalkd.bat',
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
