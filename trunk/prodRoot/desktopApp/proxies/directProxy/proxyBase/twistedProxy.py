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
        '''
        if key.lower() == "content-type":
            if value.split(';')[0] == 'text/html':
                self.parser = WordParser()
        '''
        global DEBUG_FLAG
        if DEBUG_FLAG:
            print key, value

    def handleResponsePart(self, data):
        '''
        Handle the data of the request
        '''
        proxy.ProxyClient.handleResponsePart(self, data)
        '''
        if hasattr(self, 'parser'): self.parser.feed(data)
        '''
        '''
        This function will be called when http response data got.
        '''
        '''
        global DEBUG_FLAG
        if DEBUG_FLAG:
            f = open('d:/g.html.gz','wb')
            f.write(data)
            f.close()
        '''
    def handleResponseEnd(self):
        proxy.ProxyClient.handleResponseEnd(self)
        '''
        if hasattr(self, 'parser'):
            self.parser.close()
            self.father.wordCounter.addWords(self.parser.getWords())
            del(self.parser)
        '''
        global DEBUG_FLAG
        DEBUG_FLAG = False


class cacheProxyClientFactory(proxy.ProxyClientFactory):
    def buildProtocol(self, addr):
        client = proxy.ProxyClientFactory.buildProtocol(self, addr)
        #upgrade proxy.proxyClient object to cacheProxyClient
        client.__class__ = cacheProxyClient
        return client


class cacheProxyRequest(proxy.ProxyRequest):
    '''
    Initiate the proxy client factory for the request, self.process will be called and new connection will
    be made to get the real data. And the new connection will be handled by the client generated by 
    proxy client factory
    '''
    protocols = {'http': cacheProxyClientFactory}
    def __init__(self, *args):
        proxy.ProxyRequest.__init__(self, *args)



class cacheProxy(proxy.Proxy):
    def __init__(self):
        proxy.Proxy.__init__(self)
    def requestFactory(self, *args):
        return cacheProxyRequest(*args)



class cacheProxyFactory(http.HTTPFactory):
    def __init__(self):
        http.HTTPFactory.__init__(self)
    def buildProtocol(self, addr):
        protocol = cacheProxy()
        return protocol


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    from twisted.internet import reactor
    proxyFct = cacheProxyFactory()
    reactor.listenTCP(PROXY_PORT, proxyFct)
    reactor.run()