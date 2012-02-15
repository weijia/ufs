'''
Created on 2011-9-22

@author: Richard
'''

import threading
import Queue
import xmlrpclib
import cherrypy
from cherrypy import _cptools

class serverThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pendingQ = Queue.Queue()
    def notify(self, notifyParam):
        self.pendingQ.put((False, notifyParam))
    def quit(self):
        self.pendingQ.put((True, None))
    def run(self):
        cnt = 0
        while True:
            quitFlag, notifyParam = self.pendingQ.get()
            print 'get item', quitFlag, notifyParam
            if quitFlag:
                self.pendingQ.task_done()
                break
            if True:#try:
                print 'calling subClassRun'
                self.subClassRun(notifyParam)
                #except:
                pass
            self.pendingQ.task_done()
            
            cnt = cnt + 1
            print cnt
        print 'returning'
    def subClassRun(self, notifyParam):
        pass
    
    def notifyXmlRpcServer(self, serverUrl, param):
        proxy = xmlrpclib.ServerProxy(serverUrl)
        try:
            print proxy.notify(param)
        except:
            print 'notify with exception'
            pass

class xmlRpcServerWithWorkerThreadBase(_cptools.XMLRPCController):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.itemList = {}
        
    def register(self, threadId, threadInst):
        self.itemList[threadId] = threadInst
    #register.exposed = True
        
    def notify(self, threadId, notifyParam):
        self.itemList[threadId].notify(notifyParam)
        
    notify.exposed = True
    
    
    
def startMainServer(rpcObj, port = 8806):
    class Root:
        def index(self):
            return "I'm a standard index!"
        index.exposed = True
    root = Root()
    root.xmlrpc = rpcObj

    cherrypy.config.update({'environment': 'production',
                            'log.error_file': '../../../../site.log',
                            'log.screen': True,
                            'engine.autoreload_on' : True,
                            'server.socket_port' : port,
                            'request.dispatch': cherrypy.dispatch.XMLRPCDispatcher(),
                            'tools.xmlrpc.allow_none': 1,})

    cherrypy.quickstart(root, '/')   
    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    startMainServer(xmlRpcServerWithWorkerThreadBase())