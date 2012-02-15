from twisted.web import proxy

import localLibSys
from localLibs.logSys.logSys import *

class redirectableProxyClientFactory(proxy.ProxyClientFactory):
    def __init__(self, command, rest, version, headers, data, father, \
        proxyServer, proxyPort, uri):
        self.proxyServer = proxyServer
        self.proxyPort = proxyPort
        self.uri = uri
        self.usingProxy = False
        self.id = 0
        proxy.ProxyClientFactory.__init__(self, command, rest, version, \
            headers, data, father)
    def useProxy(self):
        cl('id:',self.id,'redirect request called')
        self.rest = self.uri
        cl('id:',self.id,'rest:%s'%self.rest)
        self.usingProxy = True
        from twisted.internet import reactor
        reactor.connectTCP(self.proxyServer, self.proxyPort, self)
        cl('id:',self.id,'connecting relay proxy:',self.proxyServer, ':',self.proxyPort)
