from twisted.internet import reactor
import proxyFrameworkV2 as proxyFramework


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
        reactor.listenTCP(self.proxyParam.servePort, proxyFct)
        reactor.run()
        
        
if __name__ == "__main__":
    from twisted.internet import reactor
    param = {"proxyRequestFactoryClass": proxyRequestFactory,
             "proxyRequestClass":proxyRequestWithDirectConnectClient,
             "serverPort":8809
        }
    proxyFct = proxyFactory(param)
    reactor.listenTCP(param["serverPort"], proxyFct)
    reactor.run()