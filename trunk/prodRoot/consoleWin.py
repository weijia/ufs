import localLibs.logWin.advScriptRunnerV3 as scriptRunner
import localLibs.logWin.advScriptRunnerXmlRpcServer as advScriptRunnerXmlRpcServer

autoStartAppList = ['mongodb.bat',
                    'webserver-cgi',
                    'cherrypyServerV3',
                    'startBeanstalkd.bat',
                    #'folderCollectionInitiator',
                    #'collectionServiceApp.py',
                    #'collectionMonitorNonRealtimeNotifierServiceV2',
                    #'syncXmlRpcServerV2,
                    'tubeDelayService',
                    'monitorServiceV2',
                    'folderScanner'
                    ]

def main():
    scriptRunner.startApplicationsNoReturn(autoStartAppList, 
                                            advScriptRunnerXmlRpcServer.launcherXmlRpcThread)

if __name__ == "__main__":
    main()
