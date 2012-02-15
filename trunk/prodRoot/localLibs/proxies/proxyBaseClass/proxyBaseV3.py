from twisted.internet import reactor
import proxyFrameworkV3 as proxyFramework


class proxyBaseInterface:
    def __init__(self, proxyParam):
        pass
    def startServer():
        pass

        
class proxyBase(proxyBaseInterface):
    def __init__(self, proxyParam):
        self.proxyParam = proxyParam
    def startServer(self):
        '''
        Proxy step 2, create a proxy factory and listen to port
        '''
        proxyFct = proxyFramework.proxyFactory(self.proxyParam)
        reactor.listenTCP(self.proxyParam["servePort"], proxyFct)
        reactor.run()
        
'''

When connection was established, factory's buildProtocol was called


Proxy step 1, create proxy instance and start the proxy server
Proxy step 2, create a proxy factory and listen to port
Proxy Step 3, http.HTTPFactory.buildProtocol was called when connection established to this proxy server
Proxy Step 4, proxy.Proxy return a ProxyRequest
Proxy step 5, set client factory for protocol so when request data received,
        ProxyRequest can generate a client factory
        
        This file is used for step 1
        
'''
if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass":proxyFramework.proxyRequestWithDirectConnectClient,
             "servePort":8809
        }
    a = proxyBase(param)
    a.startServer()