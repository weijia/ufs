import proxyFrameworkV2 as proxyFramework
import proxyAppBaseV2 as proxyAppBase


class sampleProxyFactory(proxyFramework.customizableClientClassFactoryInterface):
    def getClientClass(self):
        return proxyFramework.directConnectProxyClient

        
if __name__ == "__main__":
    p = proxyAppBase.proxyParamBaseInterface(sampleProxyFactory)
    a = proxyAppBase.proxyAppBase(p)
    a.createProxyStart()
