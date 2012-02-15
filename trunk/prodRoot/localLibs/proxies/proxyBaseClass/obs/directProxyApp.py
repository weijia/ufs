import proxyClientBaseInterface
import proxyBaseClass

class directConnectClient(proxyClientBaseInterface.proxyClientBaseInterface):
    pass

class simpleProxyRequestFactory():


#Inherit client factory so a customizable client can be used
class directConnectClientFactory(proxyClientFactoryBase):
    def getProxyClientClass(self):
        return directConnectClient

        
        
        
if __name__ == "__main__":
    proxyBase = proxyBaseClass.proxyBaseClass(proxyFactoryBase, directConnectClientFactory)
    proxyBase.startServer()