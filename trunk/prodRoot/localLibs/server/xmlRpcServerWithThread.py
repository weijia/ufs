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



def getUuid():
    return unicode(str(uuid.uuid4()))

class serverThread(threading.Thread):
    def __init__(self, threadHndl = getUuid(), 
                 clientId = getUuid(), paramDict = {}):
        '''
        threadHndl should be identical for thread, it is to say that one thread will have 1 callba
        '''
        self.paramDict = copy.copy(paramDict)
        self.paramDict["clientId"] = clientId
        self.paramDict["threadHndl"] = threadHndl
        self.listenerList = {}
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.pendingQ = Queue.Queue()
        self.ClientId = clientId
        self.threadHndl = threadHndl
        self.listenerList[self.ClientId] = self.paramDict

    ###################################
    # The following functions can be called by external objects
    # and can be called thread safe
    ###################################
    def msg(self, method, msgDict):
        ncl(method, msgDict)
        self.pendingQ.put((method, msgDict))

    ##################################
    # The following are only for internal use, will only be called from manager server
    ##################################
    def getThreadHndl(self):
        '''
        threadHndl is an id for every working thread, so it SHOULD be identical
        if the thread will do the same work
        '''
        return self.threadHndl
    
    def getFirstClientId(self):
        '''
        processorHndl is an id for every task, a thread may be running several tasks
        '''
        return self.ClientId
    
    def getParamDict(self):
        return self.paramDict
    
    def addListener(self, newProcessor):
        paramDict = newProcessor.getParamDict()
        clientId = newProcessor.getFirstClientId()
        self.listenerList[clientId] = copy.copy(paramDict)
        return clientId
    
    ##################################
    # The following are only for internal use, will only be called from 
    # this class itself, calling these methods by sending message 
    # to this class with no "Internal"
    ##################################
    def exitThreadInternal(self, opParam):
        self.quitFlag = True
        return True
    
    def subClassRunInternal(self, opParam):
        return self.subClassRun(opParam)
    
    def isExisting(self):
        return self.quitFlag
    
    def run(self):
        cnt = 0
        while True:
            op, opParam = self.pendingQ.get()
            cl('get item', op, opParam)
            #Calling internal function: complete will be completeInternal
            opFunc = getattr(self, op+"Internal")
            
            quitFlag = opFunc(opParam)
            self.pendingQ.task_done()
            if quitFlag:
                #The following is not needed as opFunc set this already
                self.quitFlag = True
                cl("quit flag set, return from thread")
                break
            cnt = cnt + 1
            cl("processed msg count:", cnt)
        print 'returning'


class xmlRpcServerWithThread(xmlRpcServerBase.managedXmlRpcServerBase):
    '''
    classdocs
    '''
    def __init__(self, port):
        '''
        Constructor
        '''
        self.thread2Processor = {}
        self.thread2ClientId = {}
        #self.threadHndlAndProcessorHndl2ThreadDict = {}
        xmlRpcServerBase.managedXmlRpcServerBase.__init__(self, port)
        

    def createProcessor(self, newProcessor):
        '''
        Working thread can accept more than 1
        '''
        #newThread = self.workingThreadClass(paramDict)
        threadHandle = newProcessor.getThreadHndl()
        clientId = newProcessor.getFirstClientId()
        cl("register called")
        if self.thread2ClientId.has_key(threadHandle):
            existingProcessor = self.thread2Processor[threadHandle]
            #Callback handler exists, check if it is duplicated registration
            if clientId in self.thread2ClientId[threadHandle]:
                cl("Already registered")
                return threadHandle
            else:
                cl("New listener")
                existingProcessor.addListener(newProcessor)
                self.thread2ClientId[threadHandle].append(clientId)
                return clientId
        else:
            cl("New Processor")
            self.thread2ClientId[threadHandle] = [clientId]
            self.thread2Processor[threadHandle] = newProcessor
            newProcessor.start()
            #newProcessor.msg("subClassRun", {})
            ncl('returnning:', threadHandle)
            return threadHandle
    def getThreadInst(self, threadHandle):
        return self.thread2Processor[threadHandle]
        
    def stop(self):
        cl('-----------------------exist server called')
        for threadHandle in self.thread2Processor:
            self.thread2Processor[threadHandle].msg("exitThread", {})
    stop.exposed = True
    


    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(xmlRpcServerWithThread(gXmlRpcServerPort))