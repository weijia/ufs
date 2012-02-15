import libSys
from twisted.web import proxy
import proxyBaseClass.proxyFrameworkV3 as proxyFramework
import proxyBaseClass.proxyAppBaseV3 as proxyAppBase
#import urlparse
import simpleLoadBalancingProxy as baseLoadBalancing


class loadBalanceProxyClient(baseLoadBalancing.stateProxyClient):
    '''
    This class is used to handle content returned by web server
    '''
    def handleResponseEnd(self):
        print 'end of handle response'
        try:
            proxy.ProxyClient.handleResponseEnd(self)
        except:
            self.proxyParam["curServerIndex"] = (self.proxyParam["curServerIndex"] + 1)%len(self.proxyParam["serverHosts"])
            print 'proxy switched to index:', self.proxyParam["curServerIndex"]
            print 'exception, maybe server disconnected'
            print "session info:",self.sessionParam
            pass

    
class loadBalancingProxyRequest(baseLoadBalancing.simpleLoadBalancingProxyRequest):
    def getAvailServer(self):
        pair = None
        #Find an available server first
        for i in self.proxyParam["serverHosts"]:
            if i in self.proxyParam["abnormalHosts"]:
                continue
            pair = i
            break
        #pair = self.proxyParam["serverHosts"][0]
        print "using:",pair
        return pair
    

class loadBalanceClientFactory(baseLoadBalancing.clientFactoryWithSession):
    '''
    def clientConnectionLost(self, connector, reason):
        print 'clientConnectionLost'
        baseLoadBalancing.clientFactoryWithSession.clientConnectionLost(self, connector, reason)
        self.proxyParam["curServerIndex"] = (self.proxyParam["curServerIndex"] + 1)%len(self.proxyParam["serverHosts"])
        print 'proxy switched to index:', self.proxyParam["curServerIndex"]
        '''
    def getClientClass(self):
        self.proxyParam["curServerIndex"] = 0
        return loadBalanceProxyClient
        
        
if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": loadBalancingProxyRequest,
             "clientFactoryClass": loadBalanceClientFactory,
             #"serverHost":"127.0.0.1",
             #"serverHost":"wwwgate0-ch.mot.com",
             "serverHosts":["127.0.0.1:3128", "wwwgate0.mot.com:1080"],
             #"serverPort":1080,
             "servePort":8809,
             "abnormalHosts":[]
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
