'''
Created on 2011-10-11

@author: Richard
'''
from cherrypy import _cptools
import cherrypy
import xmlrpclib


import localLibSys
from localLibs.logSys.logSys import *

gTaskManagerXmlRpcServerUrl = u"http://127.0.0.1:8810/xmlrpc"


def registerToTaskManager(selfServerUrl):
    proxy = xmlrpclib.ServerProxy(gTaskManagerXmlRpcServerUrl)
    try:
        proxy.register(selfServerUrl)
    except:
        cl('notify with exception')
        pass

class xmlRpcServerBase(_cptools.XMLRPCController):
    '''
    classdocs
    '''
    def __init__(self, port):
        '''
        Constructor
        '''
        self.port = port
        print self.port
        _cptools.XMLRPCController.__init__(self)
        
    def getServerPort(self):
        return self.port
    
    def getSelfServerUrl(self, port):
        return "http://127.0.0.1:%d/xmlrpc"%self.getServerPort()

class managedXmlRpcServerBase(xmlRpcServerBase):
    def __init__(self, port):
        xmlRpcServerBase.__init__(self, port)
        registerToTaskManager(self.getSelfServerUrl(port))
    
def startMainServer(rpcObj):
    class Root:
        def index(self):
            return "I'm a standard index!"
        index.exposed = True
    root = Root()
    root.xmlrpc = rpcObj
    cherrypy.engine.subscribe("stop", rpcObj.stop)
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': '../../../../site.log',
                            'log.screen': True,
                            'engine.autoreload_on' : True,
                            'server.socket_port' : rpcObj.getServerPort(),
                            'request.dispatch': cherrypy.dispatch.XMLRPCDispatcher(),
                            'tools.xmlrpc.allow_none': 1,})

    cherrypy.quickstart(root, '/')
    
    