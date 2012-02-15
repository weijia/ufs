'''
Created on 2011-9-22

@author: Richard
'''

import localLibSys
from localLibs.logSys.logSys import *
import xmlRpcServerBase

gXmlRpcServerPort = 8901
gXmlRpcServerUrl = u"http://127.0.0.1:%d/xmlrpc"%gXmlRpcServerPort

import xmlRpcServerWithThread as threadSvrBase

class sampleThread(threadSvrBase.serverThread):
    def __init__(self, threadHndl = threadSvrBase.getUuid(), 
                 clientId = threadSvrBase.getUuid(), paramDict = {}):
        super(sampleThread, self).__init__(threadHndl,
                                                       clientId,
                                                       paramDict)
    def sampleMethodInternal(self, clientId):
        #Server will send message to this class and the
        #parent class will generate call to member in
        #a message loop
        print "Sample method called:", clientId

class sampleServer(threadSvrBase.xmlRpcServerWithThread):
    '''
    classdocs
    '''
    def __init__(self, port):
        '''
        Constructor
        '''
        super(sampleServer, self).__init__(port)
        
    def sampleCreateOnServer(self):
        threadInst = sampleThread(clientId = "helloworld")
        return self.createProcessor(threadInst)
    sampleCreateOnServer.exposed = True
    
    def sampleMethod(self, threadHandle, clientId = "helloworld"):
        cl(threadHandle, clientId)
        t = self.thread2Processor[(threadHandle)]
        t.msg("sampleMethod", {"clientId":clientId})
    sampleMethod.exposed = True
    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(sampleServer(gXmlRpcServerPort))