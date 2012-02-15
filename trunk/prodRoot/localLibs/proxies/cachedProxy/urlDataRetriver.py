import os
from twisted.web import proxy
from twisted.internet import reactor


from hostStateManager import hostStateManager
from fullProxyClient import *
from headerProxyClient import *
from redirectableProxyClientFactory import *
hMan = hostStateManager()


import localLibSys
from localLibs.logSys.logSys import *

RECONNECT_TIME = 6


class cacheProxySmartClientFactory(redirectableProxyClientFactory):
    def __init__(self, *args):
        self.id = None
        self.writtenDataLength = 0
        self.transferingData = False
        self.clientClass = fullProxyClient
        self.hostStateQueryId = hMan.getHostStateQueryId()
        redirectableProxyClientFactory.__init__(self, *args)

    def buildProtocol(self, addr):
        self.client = client = redirectableProxyClientFactory.buildProtocol(self, addr)
        #upgrade proxy.proxyClient object to cacheProxyClient
        #This class will be used to handle the server response of the client request
        client.__class__ = self.clientClass
        client.smartClientFactory = self
        printLog('id:',self.id,'protocol built')
        return client

    def clientConnectionFailed(self, connector = None, reason = None):
        if not self.usingProxy:
            hMan.addFailRecord(self.uri)
        printLog('id:',self.id,'connection fail called')
        self.failedToRetrieve()
        
    def handleStatus(self, version, code, message):
        printLog('in factory, id:',self.id,'status got')
        self.clientClass = headerProxyClient
        
    def handleEndHeaders(self):
        self.clientClass = dataProxyClient
        
    def writeData(self, curPos, data):
        cachePath = url2dir(self.uri, 'd:/cache/')
        #Write data write log
        #printLog('id:',self.id,'data received')
        o = open(os.path.join(cachePath,'log.txt'),'ab')
        print >>o, 'write at',curPos,'len:',len(data),'\r\n'
        o.close()
        #Update the real data
        f = open(os.path.join(cachePath,'content'+ self.client.info['ext']),'ab')#use ab, so will not truncate the file.
        f.seek(curPos)
        f.write(data)
        #print 'writing:', cachePath,'curP:',curPos
        f.close()
        #Send proper data to client
        if self.writtenDataLength > curPos:
            off = self.writtenDataLength - curPos
            if off < len(data):
                self.writeRealData(data[off:])
        elif self.writtenDataLength == curPos:
            self.writeRealData(data)
        else:
            printLog('id:',self.id, 'cur:%d, got:%d'%(self.writtenDataLength,curPos))
    def writeRealData(self, data):
        self.father.transport.write(data)
        self.writtenDataLength += len(data)
        cl('id:',self.id,',', self.writtenDataLength, ',written')
        
    def failedToRetrieve(self):
        if hMan.requestConnectionPermission(self.hostStateQueryId, self.uri):
            #The function call returned True, then we have the connection request
            #recorded in host state manager
            from twisted.internet import reactor
            reactor.callLater(RECONNECT_TIME, self.useProxy)
        else:
            from twisted.internet import reactor
            reactor.callLater(RECONNECT_TIME, self.failedToRetrieve)
            
class urlDataRetriver:
    def __init__(self, host, port, factory):
        self.host = host
        self.port = port
        self.factory = factory
        from twisted.internet import reactor
        reactor.callLater(1, self.retieve)
    def retieve(self):
        if hMan.preCheckUrl(self.factory.uri):
            #Direct connect first
            print 'id: %d, direct first'%self.factory.id
            reactor.connectTCP(self.host, self.port, self.factory)
        else:
            print 'id: %d, proxy always'%self.factory.id
            self.factory.useProxy()
