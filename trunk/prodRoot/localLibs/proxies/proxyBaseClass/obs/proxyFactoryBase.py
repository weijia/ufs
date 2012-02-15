from twisted.web import proxy, http




class proxyClassBaseClassInternal(proxy.Proxy):
    '''
    Used to generate the proxy request, it is a default protocol for add custmizable proxy client
    '''
    def __init__(self, proxyRequestClass, proxyClientFactory):
        self.proxyRequestClass = proxyRequestClass
        self.proxyClientFactory = proxyClientFactory
        proxy.Proxy.__init__(self)
    def requestFactory(self, *args):
        '''
        Proxy step 4, create a proxy request factory
        '''
        return self.proxyRequestClass(self.proxyClientFactory, *args)



class proxyFactoryInterface(http.HTTPFactory):
    def __init__(self, proxyClass):
        pass
        
    def buildProtocol(self, addr):
        pass

class proxyFactoryBase(proxyFactoryInterface):
    def __init__(self, proxyRequestClass, proxyClient):
        #It will be used to generate a proxy request
        self.proxyRequestClass = proxyRequestClass
        #It will be passed to the proxy request class, so a custom proxy client (proxyClientFactory) can be used as a client factory
        self.proxyClientFactory = clientCustomizableProxyRequestClass(proxyClient)
        http.HTTPFactory.__init__(self)
        
    def buildProtocol(self, addr):
        '''
        Proxy step 3, create protocol/proxy request factory when connection established
        '''
        protocol = self.proxyClassBaseClassInternal(self.proxyRequestClass, self.proxyClientFactory)
        return protocol
