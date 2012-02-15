from twisted.web import proxy
import urlparse

import localLibSys
import proxyFrameworkV3 as proxyFramework
import proxyAppBaseV3 as proxyAppBase

import localLibSys
from localLibs.logSys.logSys import *


class cachedClientRequest(proxyFramework.proxyRequestWithDirectConnectClient):
    '''
    This will override process funcion of proxyRequest and will pass an additional param to client factory
    '''
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        host = parsed[1]
        port = self.ports[protocol]
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        rest = urlparse.urlunparse(('', '') + parsed[2:])
        if not rest:
            rest = rest + '/'
        ###############################-Mod start
        #The original client factory class will be get from self.protocols
        #class_ = self.protocols[protocol]
        #Now it will be get from self.proxyParam
        class_ = self.proxyParam["clientFactoryClass"]
        ###############################-Mod End
        headers = self.getAllHeaders().copy()
        if 'host' not in headers:
            headers['host'] = host
        self.content.seek(0, 0)
        s = self.content.read()
        ###############################-Mod start
        #clientFactory = class_(self.method, rest, self.clientproto, headers,
        #                       s, self)
        clientFactory = class_(self.proxyParam, self.method, rest, self.clientproto, headers,
                               s, self)
        ###############################-Mod End
        self.reactor.connectTCP(host, port, clientFactory)


    def connectionLost(self, reason):
        """connection was lost"""
        printLog('id:',self.id,'----------------client connection lost')
        self.connectionLostCallback()
    def write(self, data):
        printLog('id:',self.id,'writing data')
        proxy.ProxyRequest.write(self, data)
    def finish(self):
        printLog('id:',self.id,'finish called')
        proxy.ProxyRequest.finish(self)
    def connectionLostCallback(self):
        pass



class cachedClientFactory(proxyFramework.customizableClientClassFactoryInterface):
    def __init__(self, proxyParam, *args):
        self.proxyParam = proxyParam
        proxyFramework.customizableClientClassFactoryInterface.__init__(self, *args)

if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": cachedClientRequest,
             "clientFactoryClass": cachedClientFactory,
             "servePort":8809
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
