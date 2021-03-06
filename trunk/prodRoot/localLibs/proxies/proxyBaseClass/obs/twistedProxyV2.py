from twisted.web import proxy, http

#-------------------------------------------------------------------------------



PROXY_PORT = 8809
#-------------------------------------------------------------------------------
DEBUG_FLAG = False
#-------------------------------------------------------------------------------


class cacheProxyClient(proxy.ProxyClient):
    '''
    This class is used to handle content returned by web server
    '''
    def handleHeader(self, key, value):
        proxy.ProxyClient.handleHeader(self, key, value)


    def handleResponsePart(self, data):
        '''
        Handle the data of the request
        '''
        proxy.ProxyClient.handleResponsePart(self, data)

    def handleResponseEnd(self):
        proxy.ProxyClient.handleResponseEnd(self)

        

class customizableClientClassFactoryInterface(proxy.ProxyClientFactory):
    def buildProtocol(self, addr):
        client = proxy.ProxyClientFactory.buildProtocol(self, addr)
        #upgrade proxy.proxyClient object to cacheProxyClient
        client.__class__ = self.getClientClass()
        return client
    def getClientClass(self):
        return cacheProxyClient
        
        
class cachedClientClassFactory(customizableClientClassFactoryInterface):
    def getClientClass(self):
        return cacheProxyClient
        

class customizableClientFactoryProxyRequest(proxy.ProxyRequest):
    '''
    Initiate the proxy client factory for the request, self.process will be called and new connection will
    be made to get the real data. And the new connection will be handled by the client generated by 
    proxy client factory
    '''
    #self.protocols will be used to retrieve the client factory, init it dynamically so we can assign dynamic proxy client
    #protocols = {'http': proxyClientFactory}
    def __init__(self, proxyClientFactoryClass, *args):
        '''
        Proxy step 5, init a proxy request
        '''
        self.protocols = {'http': proxyClientFactoryClass}
        proxy.ProxyRequest.__init__(self, *args)



class proxyRequestFactory(proxy.Proxy):
    def __init__(self, proxyClientFactoryClass):
        self.proxyClientFactoryClass = proxyClientFactoryClass
        proxy.Proxy.__init__(self)
    def requestFactory(self, *args):
        return customizableClientFactoryProxyRequest(self.proxyClientFactoryClass, *args)



class proxyFactory(http.HTTPFactory):
    def __init__(self, proxyClientFactoryClass):
        self.proxyClientFactoryClass = proxyClientFactoryClass
        http.HTTPFactory.__init__(self)
    def buildProtocol(self, addr):
        '''
        Step 3, called when connection established to this proxy server
        '''
        protocol = proxyRequestFactory(self.proxyClientFactoryClass)
        return protocol


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    from twisted.internet import reactor
    proxyFct = proxyFactory(cachedClientClassFactory)
    reactor.listenTCP(PROXY_PORT, proxyFct)
    reactor.run()