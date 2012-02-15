'''
Created on 2011-9-22

@author: Richard
'''

import threading
import Queue
import xmlrpclib
import cherrypy
#from cherrypy import _cptools
import uuid
#import cherrypy.engine

import localLibSys
from localLibs.logSys.logSys import *
import xmlRpcServerBase
import copy

gXmlRpcServerPort = 8806
gXmlRpcServerUrl = u"http://127.0.0.1:%d/xmlrpc"%gXmlRpcServerPort


import xmlRpcServerWithThread as svrBase

class xmlRpcNotifier(svrBase.serverThread):
    def __init__(self, threadHndl = svrBase.getUuid(), 
                 clientId = "http://127.0.0.1:8898/xmlrpc", paramDict = {}):
        '''
        threadHndl should be identical for thread, it is to say that one thread will have 1 callba
        '''
        super(xmlRpcNotifier, self).__init__(threadHndl, clientId)
        self.paramDict["callbackServerUrl"] = clientId
        self.firstServerUrl = clientId
        
        
    ##################################
    # The following are only for internal use, will only be called from 
    # this class itself, calling these methods by sending message 
    # to this class with no "Internal"
    ##################################
    def completeInternal(self, opParam):
        #This is the folder we are expecting to get list from, will be folder://C:/xxxx/xxx
        cl(opParam)
        del self.listenerList[opParam["clientId"]]["waitingForResponse"]
        return False

    ####################################
    # Tool function used to notify xml rpc server
    # only called internally
    ####################################
    def notifyAll(self):
        cl("listenerDict", self.listenerList)
        for i in self.listenerList:
            #Only send notify if the server has send response to previous notification
            if not self.listenerList[i].has_key("waitingForResponse"):
                if True:#try:
                    if self.listenerList[i]["callbackServerUrl"] is None:
                        continue
                    cl('notifying', self.listenerList[i]["callbackServerUrl"], self.threadHndl)
                    self.notifyXmlRpcServer(self.listenerList[i]["callbackServerUrl"], self.threadHndl)
                    self.listenerList[i]["waitingForResponse"] = True
                    cl("listenerDict", self.listenerList)
                #except 
            else:
                cl("notification sent already", i, self.listenerList[i])
            
    def notifyXmlRpcServer(self, serverUrl, param):
        cl("notifying:", serverUrl, param)
        proxy = xmlrpclib.ServerProxy(serverUrl)
        try:
            proxy.notify(param)
        except:
            cl('notify with exception')
            pass
    ###################################
    # For sub class
    ###################################
    def subClassRun(self, notifyParam):
        '''
        Sub class should override this method to do real processing
        '''
        pass



class notifierServer(svrBase.xmlRpcServerWithThread):
    def complete(self, threadHandle, clientId):
        cl(threadHandle, clientId)
        t = self.thread2Processor[threadHandle]
        t.complete({"clientId":clientId})
    complete.exposed = True
