#import gobject
import threading
#import gtk
import cherrypy
#from cherrypy import _cptools
#import sys
import xmlrpclib
import socket
#import time


import advScriptRunnerV3 as advScriptRunner
import localLibSys
#import localLibs.server.xmlRpcServerWithWorkerThreadBaseV2 as xmlRpcServerWithThreadBase
from localLibs.logSys.logSys import *
import localLibs.server.xmlRpcServerBase as xmlRpcServerBase

def startApp(target, dbusArrayAppAndParamList):
        print 'start app called'
        appAndParamList = []
        for i in dbusArrayAppAndParamList:
            appAndParamList.append(str(i))
        target.addAppToIdleRunner(appAndParamList)
        print 'calling app done'
        return 'done'


class launcherXmlRpcServer(xmlRpcServerBase.xmlRpcServerBase):
    '''
    classdocs
    '''
    def __init__(self, target, port):
        '''
        Constructor
        '''
        self.target = target
        self.appList = {}
        self.port = port
        xmlRpcServerBase.xmlRpcServerBase.__init__(self, port)
    def start(self, appAndParamList):
        startApp(self.target, appAndParamList)
    start.exposed = True
    def register(self, callbackServerUrl):
        self.appList[callbackServerUrl] = callbackServerUrl
        ncl(callbackServerUrl, "registered")
    register.exposed = True
    def stop(self):
        #cherrypy.server.stop()
        pass
    def stopAllTasks(self):
        '''
        import sys
        sys.exit()
        '''
        for i in self.appList:
            proxy = xmlrpclib.ServerProxy(i)
            cl('stopping', i)
            try:
                proxy.stop()
            except socket.error:
                cl('stop with exception')
                pass
            '''
            except:
                cl("other exception when stopping")
            '''
        cherrypy.server.stop()
        cl('launcherXmlRpcServer stop called')
        #sys.exit()
        time.sleep(3)
        print 'exit called'

    stopAllTasks.exposed = True

    
class launcherXmlRpcThread(threading.Thread):
    def __init__(self, target):
        self.target = target
        threading.Thread.__init__(self)
    def run(self):
        #Connect to server
        self.server = launcherXmlRpcServer(self.target, 8810)
        xmlRpcServerBase.startMainServer(self.server)
        print 'quit running launcherXmlRpcThread(self.target)'
    def stop(self):
        #cherrypy.server.stop()
        self.server.stop()
    def stopAllTasks(self):
        self.server.stopAllTasks()
  
def main():
    advScriptRunner.startApplicationsNoReturn([], launcherXmlRpcThread)

if __name__ == "__main__":
    main()
