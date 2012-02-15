import proxyFrameworkV3 as proxyFramework
import proxyAppBaseV3 as proxyAppBase
import urlparse

class advProxyRequest(proxyFramework.proxyRequestWithDirectConnectClient):
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

class advClientFactory(proxyFramework.customizableClientClassFactoryInterface):
    def __init__(self, proxyParam, *args):
        self.proxyParam = proxyParam
        proxyFramework.customizableClientClassFactoryInterface.__init__(self, *args)


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
             "proxyRequestClass": advProxyRequest,
             "clientFactoryClass": advClientFactory,
             "servePort":8809
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
