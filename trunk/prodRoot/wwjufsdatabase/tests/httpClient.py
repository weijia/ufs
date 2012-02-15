import socket



server = "localhost"
port = 8802url = "/webapproot/static/test/testStatic.html"
#url = "/webapproot/apps/localServer/fileManagerV3.py"
url="/webapproot/static/index.html"
url="/apps/collection/jstreeOnCollectionV2.py?collectionId=ufsFs\\0//q19420-01/D\\0/tmp"
port = 9901
get_string = "GET %s HTTP/1.1\r\n\r\n"%url
    
f = None
    
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor
from sys import stdout
class Echo(Protocol):
    def dataReceived(self,data):
        f.write(data)
    def connectionMade(self):
        print 'sending line'
        global f
        f = open("d:/dump.obj","wb")
        self.transport.write(get_string)
        
class EchoClientFactory(ClientFactory):
    def startedConnecting(self,connector):
        print("Start to connect")
    def buildProtocol(self,addr):
        print("build protocol")
        return Echo()
    def clientConnectionLost(self,connector,reason):
        print("client connection lost" + str(reason))
        f.close()
        #ReconnectingClientFactory.clientConnectionLost(self,connector,reason)
    def clientConnectionFailed(self,connector,reason):
        print("client connection failed" + str(reason))
        #ReconnectingClientFactory.clientConnectionFailed(self,connector,reason)
    
reactor.connectTCP(server,port,EchoClientFactory())
reactor.run()