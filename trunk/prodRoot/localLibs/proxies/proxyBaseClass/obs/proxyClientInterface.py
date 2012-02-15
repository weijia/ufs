class proxyClientBaseInterface(proxy.ProxyClient):
    '''
    This class is used to handle content returned by web server
    '''
    def handleHeader(self, key, value):
        '''
        Handle the header of the request
        '''
        pass
    def handleResponsePart(self, data):
        '''
        Handle the data of the request
        '''
        pass
    def handleResponseEnd(self):
        proxy.ProxyClient.handleResponseEnd(self)
        pass
        
