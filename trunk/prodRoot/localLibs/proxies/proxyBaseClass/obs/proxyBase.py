from twisted.internet import reactor
import proxyFramework



class proxyBaseInterface:
    def __init__(self, clientFactoryClass, proxyRequestFactoryClass = proxyFramework.proxyRequestFactory, servePort = 8809):
        pass
    def startServer():
        pass

        
class proxyBase(proxyBaseInterface):
    def __init__(self, clientFactoryClass, proxyRequestFactoryClass, servePort = 8809):
        self.servePort = servePort
        self.clientFactoryClass = clientFactoryClass
        self.proxyRequestFactoryClass = proxyRequestFactoryClass
    def startServer(self):
        '''
        Proxy step 2, create a proxy factory and listen to port
        '''
        proxyFct = proxyFramework.proxyFactory(self.clientFactoryClass, self.proxyRequestFactoryClass)
        reactor.listenTCP(self.servePort, proxyFct)
        reactor.run()
