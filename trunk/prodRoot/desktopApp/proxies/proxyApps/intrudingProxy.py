import proxyFrameworkV3 as proxyFramework
import proxyAppBaseV3 as proxyAppBase
import urlparse
import relayProxy as relayProxy
from twisted.web import proxy

class intrudingProxyClient(proxy.ProxyClient):
    '''
    This class is used to handle content returned by web server
    '''
    def handleHeader(self, key, value):
        print 'head got:',key, value
        self.heads[key] = value
        '''
        if key == 'Content-Length':
            print 'supress length:', value
            return
        '''
        #proxy.ProxyClient.handleHeader(self, key, value)


    def handleResponsePart(self, data):
        '''
        Handle the data of the request
        '''
        #print 'data got:', data
        self.intrudingData += data
        #proxy.ProxyClient.handleResponsePart(self, data)

    def handleResponseEnd(self):
        if not self.intruded:
            self.intruded = True
            import StringIO
            compressedstream = StringIO.StringIO(self.intrudingData)
            import gzip
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
            intrudedData = data.replace('</head>','''<script>alert("OK");</script></head>''')
            #print 'replace head to', intrudedData
            
            compressingstream = StringIO.StringIO()
            gzipper = gzip.GzipFile(fileobj=compressingstream, mode='wb')
            gzipper.write(intrudedData)
            gzipper.close()
            data = compressingstream.getvalue()
            for i in self.heads:
                if i == 'Content-Length':
                    print 'supress length:', self.heads[i], len(data)
                    value = len(data)
                else:
                    value = self.heads[i]
                proxy.ProxyClient.handleHeader(self, i, value)
            proxy.ProxyClient.handleResponsePart(self, data)
            print 'handle response part end'
        try:
            proxy.ProxyClient.handleResponseEnd(self)
        except:
            print 'exception, maybe server disconnected'
            pass
    def initParam(self):
        self.intruded = False
        self.intrudingData = ''
        self.heads = {}

class intrudingClientFactory(relayProxy.advClientFactory):
    def buildProtocol(self, addr):
        client = proxy.ProxyClientFactory.buildProtocol(self, addr)
        #upgrade proxy.proxyClient object to custom client class
        client.__class__ = self.getClientClass()#This returns a class not an instance
        client.initParam()
        return client

    def getClientClass(self):
        return intrudingProxyClient

if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": relayProxy.advProxyRequest,
             "clientFactoryClass": intrudingClientFactory,
             #"serverHost":"127.0.0.1",
             "serverHost":"wwwgate0-ch.mot.com",
             "serverPort":1080,
             "servePort":8808,
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
