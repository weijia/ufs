from twisted.web import proxy
from cacheManager import *
from urlDataRetriver import *
from logSys import *
import urlparse
from proxyExtraHandler import *

globalCount = 0
cMan = cacheManager()

class cacheProxySmartRequest(proxy.ProxyRequest):
    protocols = {'http': cacheProxySmartClientFactory}
    def __init__(self, proxyServer, proxyPort,*args):
        self.proxyServer = proxyServer
        self.proxyPort = proxyPort
        global globalCount
        globalCount +=1
        self.id = globalCount
        proxy.ProxyRequest.__init__(self, *args)
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        cl('final url',self.uri)
        protocol = parsed[0]
        host = parsed[1]

        try:
            port = self.ports[protocol]
        except KeyError:
            printLog('no protol for: %s'%protocol)
            port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        rest = urlparse.urlunparse(('','')+parsed[2:])
        if not rest:
            rest = rest+'/'
        headers = self.getAllHeaders().copy()
        if not headers.has_key('host'):
            headers['host'] = host
        self.content.seek(0, 0)
        s = self.content.read()
        #Check extra handler
        if parsed[1] == 'wwj':
            proxyExtraHandler(self.uri, self, s)
        else:
            #First check cache manager
            cC = cMan.getCacheClient(self.uri)
            #If cached, send response and return
            if cC != None:
              print 'cc is not none'
              #We have the object cached, send it and return
              clientFactory = cacheClientFactory(self.method, rest, self.clientproto, headers,
                                   s, self)
              client = clientFactory.buildProtocol(host)
              client.id = self.id
              if cC.sendResponse(client):
                return 
            #The object is not cached, create cacheProxySmartClientFactory
            try:
                class_ = self.protocols[protocol]
            except KeyError:
                class_ = cacheProxySmartClientFactory
            clientFactory = class_(self.method, rest, self.clientproto, headers,
                                   s, self, self.proxyServer, self.proxyPort,
                                   self.uri)
            global globalCount
            clientFactory.id = globalCount
            urlDataRetriver(host, port, clientFactory)

    def connectionLost(self, reason):
        """connection was lost"""
        printLog('id:',self.id,'----------------client connection lost')
        self.connectionLostCallback()
    def write(self, data):
        printLog('id:',self.id,'writing data')
        proxy.ProxyRequest.write(self, data)
    def finish(self):
        printLog('id:',self.id,'finish called')
        proxy.ProxyRequest.finish(self)
    def connectionLostCallback(self):
        pass