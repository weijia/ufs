import proxyFrameworkV3 as proxyFramework
import proxyAppBaseV3 as proxyAppBase
import urlparse

class advProxyRequest(proxyFramework.proxyRequestWithDirectConnectClient):
    '''
    This will override process funcion of proxyRequest and will pass an additional param to client factory
    '''
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        ##############################
        #host = parsed[1]
        host = self.proxyParam["serverHost"]
        ##############################
        #port = self.ports[protocol]
        port = self.proxyParam["serverPort"]
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
        clientFactory = class_(self.proxyParam, self.method, rest, self.clientproto, headers,
                               s, self)
        ###############################-Mod End
        self.reactor.connectTCP(host, port, clientFactory)

class advClientFactory(proxyFramework.customizableClientClassFactoryInterface):
    def __init__(self, proxyParam, *args):
        self.proxyParam = proxyParam
        proxyFramework.customizableClientClassFactoryInterface.__init__(self, *args)

if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": advProxyRequest,
             "clientFactoryClass": advClientFactory,
             #"serverHost":"127.0.0.1",
             "serverHost":"wwwgate0-ch.mot.com",
             "serverPort":1080,
             "servePort":8808,
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
