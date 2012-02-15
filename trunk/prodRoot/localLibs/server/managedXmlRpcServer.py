'''
Created on 2011-10-07

@author: Richard
'''

import threading
import Queue
import xmlrpclib
import cherrypy
from cherrypy import _cptools



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