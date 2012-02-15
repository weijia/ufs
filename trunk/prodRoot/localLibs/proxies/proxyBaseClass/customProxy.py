import proxyFramework
import proxyAppBase
import proxyBase

class customizableClientFactoryProxyRequestWithAdditionalProcess(proxyFramework.customizableClientFactoryProxyRequest):
    #Check the protocol part, so URL without http or https will not introduce error
    def process(self, *args):
        proxyFramework.customizableClientFactoryProxyRequest.process(self, *args)



class customizableProxyRquestFactory(proxyFramework.proxyRequestFactory):
    def requestFactory(self, *args):
        return customizableClientFactoryProxyRequestWithAdditionalProcess(self.proxyClientFactoryClass, *args)


if __name__ == "__main__":
    a = proxyAppBase.proxyAppBase(proxyAppBase.testProxyFactory, proxyFramework.proxyRequestFactory)
    a.createProxyStart()
