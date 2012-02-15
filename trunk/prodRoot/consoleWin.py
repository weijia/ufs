import localLibs.logWin.advScriptRunnerV3 as scriptRunner
import localLibs.logWin.advScriptRunnerXmlRpcServer as advScriptRunnerXmlRpcServer

def main():
    scriptRunner.startApplicationsNoReturn(['mongodb.bat',
                                            'webserver-cgi.py',
                                            'cherrypyServerV3.py',
                                            'folderCollectionInitiator.py',
                                            #'collectionServiceApp.py',
                                            'collectionMonitorNonRealtimeNotifierServiceV2.py',
                                            'syncXmlRpcServerV2.py'], 
                                            advScriptRunnerXmlRpcServer.launcherXmlRpcThread)

if __name__ == "__main__":
    main()
