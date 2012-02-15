'''
Created on 2011-10-11

@author: Richard
'''
import threading
#import os
import cherrypy
#from cherrypy import _cptools
from pymongo import Connection
import sys
import subprocess
CREATE_NO_WINDOW = 0x8000000

import localLibs.logWin.fileTools as fileTools
#import localLibs.server.xmlRpcServerWithWorkerThreadBaseV2 as xmlRpcServerWithThreadBase
import localLibs.server.xmlRpcServerBase as xmlRpcServerBase
from localLibs.logSys.logSys import *

class backgroundService(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target
    def run(self):
        print 'running thread'
        #os.system(self.target)
        process = subprocess.Popen(self.target, shell=False, creationflags = CREATE_NO_WINDOW)
        #wait is used to wait for the child process to complete
        process.wait()
    def stop(self):
        #cherrypy.server.stop()
        cl('--------------------------------stopping')
        connection = Connection()
        adminDb = connection["admin"]
        try:
            adminDb.command("shutdown")
        except:
            cl("shutdown exception")
        

class mongoDbStarter(xmlRpcServerBase.managedXmlRpcServerBase):
    '''
    classdocs
    '''
    def __init__(self, threadInst, port):
        self.threadInst = threadInst
        self.stopped = False
        threadInst.start()
        xmlRpcServerBase.managedXmlRpcServerBase.__init__(self, port)


    def stop(self):
        cl("stop called")
        if self.stopped:
            return
        self.stopped = True
        self.threadInst.stop()
        #cherrypy.server.stop()
        cl('----------------------------------launcherXmlRpcServer stop called')
        #sys.exit()
        #print 'exit called'
        return "server should stop"
    stop.exposed = True
        
        
p = fileTools.findFileInProduct("mongodb.bat")
t = backgroundService(p)
server = mongoDbStarter(t, 8812)
#server.start(t)
xmlRpcServerBase.startMainServer(server)