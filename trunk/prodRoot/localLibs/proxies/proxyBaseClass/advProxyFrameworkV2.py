import urlparse
from twisted.web import proxy

import proxyFrameworkV4 as proxyFramework
import proxyAppBaseV3 as proxyAppBase


class proxyRequestCreatingClientFactoryWithParam(proxyFramework.proxyRequestWithParam):
    '''
    This will override process funcion of proxyRequest and will pass an additional param to client factory
    '''
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
        class_ = self.protocols[protocol]
        headers = self.getAllHeaders().copy()
        if 'host' not in headers:
            headers['host'] = host
        self.content.seek(0, 0)
        s = self.content.read()
        clientFactory = class_(self.method, rest, self.clientproto, headers,
                               s, self)
        self.reactor.connectTCP(host, port, clientFactory)
    '''
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        host = parsed[1]
        try:
            port = self.ports[protocol]
        except KeyError:
            cl('unknown protocol', self.uri)
            return
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
        class_ = self.proxyParam["proxyClientFactoryClass"]
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

class proxyClientFactoryWithParam(proxy.ProxyClientFactory):
    def __init__(self, proxyParam, *args):
        self.proxyParam = proxyParam
        proxy.ProxyClientFactory.__init__(self, *args)
    def buildProtocol(self, addr):
        '''
        #The following is the original buildProtocol function content
        return self.protocol(self.command, self.rest, self.version,
                             self.headers, self.data, self.father)
        '''
        client = self.proxyParam["proxyClientClass"](self.proxyParam, self.command, 
                                                     self.rest, self.version,
                                                     self.headers, self.data, self.father)
        return client


class proxyClientWithParam(proxy.ProxyClient):
    def __init__(self, proxyParam, *args):
        self.proxyParam = proxyParam
        proxy.ProxyClient.__init__(self, *args)


'''
Proxy step 1, create proxy instance and start the proxy server
Proxy step 2, create a proxy factory and listen to port
Proxy Step 3, http.HTTPFactory.buildProtocol was called when connection established to this proxy server
Proxy Step 4, proxy.Proxy return a ProxyRequest
Proxy step 5, set client factory for protocol so when request data received,
        ProxyRequest can generate a client factory
        
        
        This file is used for step 2-5
        
'''

if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": proxyRequestCreatingClientFactoryWithParam,
             "proxyClientFactoryClass": proxyClientFactoryWithParam,
             "proxyClientClass": proxyClientWithParam,
             "servePort":8809,
             "curId": 0,
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
