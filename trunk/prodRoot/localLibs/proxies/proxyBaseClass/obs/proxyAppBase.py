from optparse import OptionParser
from twisted.internet import reactor
import proxyBase
import proxyFramework

class proxyAppBaseInterface:
    def __init__(self, clientClass, proxyRequestClass):
        pass

    def createProxyStart(self):
        pass

class testProxyFactory(proxyFramework.customizableClientClassFactoryInterface):
    def getClientClass(self):
        return proxyFramework.directConnectProxyClient

        
class proxyAppBase(proxyAppBaseInterface):
    def __init__(self, clientClass, proxyRequestFactoryClass = proxyFramework.proxyRequestFactory):
        parser = OptionParser()
        parser.add_option("-p", "--port", action="store", type="int", help="proxy listen port",default = 8809)
        parser.add_option("-s", "--serverPort", action="store",help="out going proxy server port",default = None)

        (options, args) = parser.parse_args()
        self.servePort = options.port
        self.serverPort = options.serverPort
        self.clientClass = clientClass
        self.proxyRequestFactoryClass = proxyRequestFactoryClass

    def createProxyStart(self):
        '''
        Proxy step 1, create proxy instance and start the proxy server
        '''
        self.proxyInst = proxyBase.proxyBase(self.clientClass, self.proxyRequestFactoryClass, self.servePort)
        self.proxyInst.startServer()
    
    
if __name__ == "__main__":
    a = proxyAppBase(testProxyFactory, proxyFramework.proxyRequestFactory)
    a.createProxyStart()
