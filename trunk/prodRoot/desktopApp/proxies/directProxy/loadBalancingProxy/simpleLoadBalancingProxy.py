from twisted.web import proxy
import libSys
import proxyBaseClass.proxyFrameworkV3 as proxyFramework
import proxyBaseClass.proxyAppBaseV3 as proxyAppBase
import urlparse
import twisted.internet.error


class stateProxyClient(proxyFramework.directConnectProxyClient):
    '''
    This class is used to handle content returned by web server
    '''
    def setParam(self, proxyParam):
        self.proxyParam = proxyParam
    def setSessionParam(self, sessionParam):
        self.sessionParam = sessionParam



class simpleLoadBalancingProxyRequest(proxyFramework.proxyRequestWithDirectConnectClient):
    '''
    This will override process funcion of proxyRequest and will pass an additional param to client factory
    '''
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        ##############################
        #host = parsed[1]
        #host = self.proxyParam["serverHosts"]
        ##############################
        #port = self.ports[protocol]
        #port = self.proxyParam["serverPorts"]
        host= self.getAvailServer()
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        ####################################################
        #rest = urlparse.urlunparse(('', '') + parsed[2:])
        rest = self.uri
        if not rest:
            rest = rest + '/'
        ###############################-Mod start
        #The original client factory class will be get from self.protocols
        #class_ = self.protocols[protocol]
        #Now it will be get from self.proxyParam
        class_ = self.proxyParam["clientFactoryClass"]
        ###############################-Mod End
        headers = self.getAllHeaders().copy()
        if 'host' not in headers:
            headers['host'] = host
        self.content.seek(0, 0)
        s = self.content.read()
        ###############################-Mod start
        #clientFactory = class_(self.method, rest, self.clientproto, headers,
        #                       s, self)
        clientFactory = class_(self.proxyParam, {"serverHost":host+":"+str(port)}, 
                                self.method, rest, self.clientproto, headers,
                                s, self)
        ###############################-Mod End
        self.reactor.connectTCP(host, port, clientFactory)
        
    def getAvailServer(self):
        pair = self.proxyParam["serverHosts"][0]
        print "using:",pair
        return pair
    

class clientFactoryWithSession(proxyFramework.customizableClientClassFactoryInterface):
    def __init__(self, proxyParam, sessionParam, *args):
        self.proxyParam = proxyParam
        #This param is used to track the info of client session.
        self.sessionParam = sessionParam
        proxyFramework.customizableClientClassFactoryInterface.__init__(self, *args)
    def buildProtocol(self, addr):
        client = proxy.ProxyClientFactory.buildProtocol(self, addr)
        #upgrade proxy.proxyClient object to custom client class
        client.__class__ = self.getClientClass()#This returns a class not an instance
        client.setParam(self.proxyParam)
        client.setSessionParam(self.sessionParam)
        return client
    def clientConnectionFailed(self, connector, reason):
        print 'clientConnectionFailed'
    def clientConnectionLost(self, connector, reason):
        #Called after the response is handled. it is not always abnormal
        if reason.check(twisted.internet.error.ConnectionDone) is None:
            print 'clientConnectionLost', reason.__class__.__name__, reason
        else:
            print 'connection closed cleanly'
    def getClientClass(self):
        return stateProxyClient

if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": simpleLoadBalancingProxyRequest,
             "clientFactoryClass": clientFactoryWithSession,
             #"serverHost":"127.0.0.1",
             #"serverHost":"wwwgate0-ch.mot.com",
             "serverHosts":["wwwgate0-ch.mot.com:1080", "wwwgate0.mot.com:1080"],
             #"serverPort":1080,
             "servePort":8809,
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
