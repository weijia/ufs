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
                 xmlRpcCallbackServerUrl = "http://127.0.0.1:8898/xmlrpc", paramDict = {}):
        '''
        threadHndl should be identical for thread, it is to say that one thread will have 1 callba
        '''
        self.firstServerUrl = xmlRpcCallbackServerUrl
        self.paramDict = copy.copy(paramDict)
        self.paramDict["callbackServerUrl"] = xmlRpcCallbackServerUrl
        self.paramDict["threadHndl"] = threadHndl
        self.listenerList = {}
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.pendingQ = Queue.Queue()
        self.callbackServerUrl = xmlRpcCallbackServerUrl
        self.threadHndl = threadHndl
        self.listenerList[self.callbackServerUrl] = self.paramDict

    ###################################
    # The following functions can be called by external objects
    # and can be called thread safe
    ###################################
    def msg(self, method, msgDict):
        cl(method, msgDict)
        self.pendingQ.put((method, msgDict))
        
    '''
    def notifyExt(self, notifyParam):
        self.pendingQ.put(("notify", notifyParam))
    '''
    def complete(self, processorHndl):
        self.pendingQ.put(("complete", processorHndl))
    '''
    def exitThreadExt(self):
        self.pendingQ.put(("exitThread", None))
    '''
        
    ##################################
    # The following are only for internal use, will only be called from manager server
    ##################################
    def getThreadHndl(self):
        '''
        threadHndl is an id for every working thread
        '''
        return self.threadHndl
    
    def getFirstCallbackServerUrl(self):
        '''
        processorHndl is an id for every task, a thread may be running several tasks
        '''
        return self.callbackServerUrl
    
    def getParamDict(self):
        return self.paramDict
    
    def addListener(self, newProcessor):
        paramDict = newProcessor.getParamDict()
        newCallbackServerUrl = newProcessor.getFirstCallbackServerUrl()
        self.listenerList[newCallbackServerUrl] = copy.copy(paramDict)
        return newCallbackServerUrl
    
    ##################################
    # The following are only for internal use, will only be called from this class itself
    ##################################
    def exitThreadInternal(self, opParam):
        self.quitFlag = True
        return True
    
    def completeInternal(self, opParam):
        cl(opParam)
        del self.listenerList[opParam]["waitingForResponse"]
        return False
    def subClassRunInternal(self, opParam):
        return self.subClassRun(opParam)
    
    def isExisting(self):
        return self.quitFlag
    
    def run(self):
        cnt = 0
        while True:
            op, opParam = self.pendingQ.get()
            print 'get item', op, opParam
            #Calling internal function: complete will be completeInternal
            opFunc = getattr(self, op+"Internal")
            
            quitFlag = opFunc(opParam)
            self.pendingQ.task_done()
            if quitFlag:
                #The following is not needed as opFunc set this already
                self.quitFlag = True
                cl("quit flag set, return from thread")
                break
            '''
            if True:#try:
                print 'calling subClassRun'
                self.subClassRun(notifyParam)
                #except:
                pass
            self.pendingQ.task_done()
            '''
            cnt = cnt + 1
            print cnt
        print 'returning'
        

    
    ####################################
    # Tool function used to notify xml rpc server
    ####################################
    def notifyAll(self):
        cl("listenerDict", self.listenerList)
        for i in self.listenerList:
            #Only send notify if the server has send response to previous notification
            if not self.listenerList[i].has_key("waitingForResponse"):
                if True:#try:
                    cl('notifying', self.listenerList[i]["callbackServerUrl"], self.threadHndl)
                    self.notifyXmlRpcServer(self.listenerList[i]["callbackServerUrl"], self.threadHndl)
                    self.listenerList[i]["waitingForResponse"] = True
                    cl("listenerDict", self.listenerList)
                #except 
            else:
                cl("notification sent already", i, self.listenerList[i])
            
    def notifyXmlRpcServer(self, serverUrl, param):
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


class xmlRpcServerWithWorkerThreadBase(xmlRpcServerBase.managedXmlRpcServerBase):
    '''
    classdocs
    '''
    def __init__(self, port):
        '''
        Constructor
        '''
        self.threadHndl2ProcessorListDict = {}
        self.threadHndlAndProcessorHndl2ThreadDict = {}
        xmlRpcServerBase.managedXmlRpcServerBase.__init__(self, port)
        

    def createProcessor(self, newProcessor):
        '''
        Working thread can accept more than 1
        '''
        #newThread = self.workingThreadClass(paramDict)
        threadHandle = newProcessor.getThreadHndl()
        callbackServerUrl = newProcessor.getFirstCallbackServerUrl()
        cl("register called")
        if self.threadHndl2ProcessorListDict.has_key(threadHandle):
            #Callback handler exists, check if it is duplicated registration
            if callbackServerUrl in self.threadHndl2ProcessorListDict[threadHandle]:
                cl("Already registered")
                return callbackServerUrl
            else:
                cl("New listener")
                newProcessorHndl = self.threadHndl2ProcessorListDict[threadHandle].addListener(newProcessor)
                self.threadHndl2ProcessorListDict[threadHandle].append(newProcessorHndl)
                self.threadHndlAndProcessorHndl2ThreadDict[(threadHandle, newProcessorHndl)] = newProcessor
                return newProcessorHndl
        else:
            cl("New Collection")
            self.threadHndl2ProcessorListDict[threadHandle] = [callbackServerUrl]
            self.threadHndlAndProcessorHndl2ThreadDict[(threadHandle, callbackServerUrl)] = newProcessor
            newProcessor.start()
            #newProcessor.msg("subClassRun", {})
            cl('returnning:', callbackServerUrl)
            return callbackServerUrl
    def stop(self):
        cl('-----------------------exist server called')
        for callbackHndl in self.threadHndl2ProcessorListDict:
            self.threadHndlAndProcessorHndl2ThreadDict[(callbackHndl, self.threadHndl2ProcessorListDict[callbackHndl][0])].msg("exitThread", {})
    stop.exposed = True
    
    def register(self, serverUrl):
        paramDict = {"serverUrl": serverUrl}
        newProcessor = serverThread(paramDict)
        return self.createProcessor(newProcessor)
    register.exposed = True
        
    def complete(self, threadHandle, processorHndl):
        cl(threadHandle, processorHndl)
        t = self.threadHndlAndProcessorHndl2ThreadDict[(threadHandle, processorHndl)]
        t.complete(processorHndl)
    complete.exposed = True



    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(xmlRpcServerWithWorkerThreadBase(gXmlRpcServerPort))