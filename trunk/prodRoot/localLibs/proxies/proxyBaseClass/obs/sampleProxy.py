import proxyFramework
import proxyAppBase


class sampleProxyFactory(proxyFramework.customizableClientClassFactoryInterface):
    def getClientClass(self):
        return proxyFramework.directConnectProxyClient

        
if __name__ == "__main__":
    a = proxyAppBase.proxyAppBase(sampleProxyFactory)
    a.createProxyStart()
