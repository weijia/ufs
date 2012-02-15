from optparse import OptionParser
from twisted.internet import reactor
import proxyBaseV2 as proxyBase
import proxyFrameworkV2 as proxyFramework

class proxyAppBaseInterface:
    def __init__(self, clientClass, proxyRequestClass):
        pass

    def createProxyStart(self):
        pass

class testProxyFactory(proxyFramework.customizableClientClassFactoryInterface):
    def getClientClass(self):
        return proxyFramework.directConnectProxyClient
        
class proxyParamBaseInterface:
    def __init__(self, proxyClientFactoryClass, 
            proxyRequestFactoryClass = proxyFramework.proxyRequestFactory, 
            servePort = 8809):
        self.proxyClientFactoryClass = proxyClientFactoryClass
        self.proxyRequestFactoryClass = proxyRequestFactoryClass
        self.servePort = servePort

        
class proxyAppBase(proxyAppBaseInterface):
    def __init__(self, proxyParam):
        self.proxyParam =  proxyParam
        parser = OptionParser()
        parser.add_option("-p", "--port", action="store", type="int", help="proxy listen port",default = 8809)
        parser.add_option("-s", "--serverPort", action="store",help="out going proxy server port",default = None)

        (options, args) = parser.parse_args()
        self.proxyParam.servePort = options.port
        self.proxyParam.serverPort = options.serverPort

    def createProxyStart(self):
        '''
        Proxy step 1, create proxy instance and start the proxy server
        '''
        self.proxyInst = proxyBase.proxyBase(self.proxyParam)
        self.proxyInst.startServer()
    
    
if __name__ == "__main__":
    a = proxyAppBase(testProxyFactory, proxyFramework.proxyRequestFactory)
    a.createProxyStart()
