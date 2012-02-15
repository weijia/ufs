from optparse import OptionParser
from twisted.internet import reactor
import proxyBaseV3 as proxyBase
import proxyFrameworkV3 as proxyFramework

class proxyAppBaseInterface:
    def __init__(self, clientClass, proxyRequestClass):
        pass

    def createProxyStart(self):
        pass

class testProxyFactory(proxyFramework.customizableClientClassFactoryInterface):
    def getClientClass(self):
        return proxyFramework.directConnectProxyClient

        
class proxyAppBase(proxyAppBaseInterface):
    def __init__(self, proxyParam = {}):
        self.proxyParam =  proxyParam
        self.setDefaultParam()
        parser = OptionParser()
        parser.add_option("-p", "--port", action="store", type="int", help="proxy listen port",default = None)
        parser.add_option("-s", "--serverPort", action="store", type="int", help="out going proxy server port",default = None)

        (options, args) = parser.parse_args()
        if not (options.port is None):
            self.proxyParam["servePort"]= options.port
        if not (options.serverPort is None):
            self.proxyParam["serverPort"] = options.serverPort

    def createProxyStart(self):
        '''
        Proxy step 1, create proxy instance and start the proxy server
        '''
        self.proxyInst = proxyBase.proxyBase(self.proxyParam)
        self.proxyInst.startServer()
    def setDefaultParam(self):
        param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
                 "proxyRequestClass":proxyFramework.proxyRequestWithDirectConnectClient,
                 "servePort":8809,
        }
        for i in param:
            if not self.proxyParam.has_key(i):
                self.proxyParam[i] = param[i]

'''
Proxy step 1, create proxy instance and start the proxy server
Proxy step 2, create a proxy factory and listen to port
Proxy Step 3, called when connection established to this proxy server
Proxy Step 4, return a proxyRequest
Proxy step 5, init a proxy request
'''
if __name__ == "__main__":
    '''
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass":proxyFramework.proxyRequestWithDirectConnectClient,
             "servePort":8809,
        }
    '''
    a = proxyAppBase(param)
    a.createProxyStart()
