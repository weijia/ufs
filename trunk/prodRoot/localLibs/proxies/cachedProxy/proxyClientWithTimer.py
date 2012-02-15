from correctHeaderProxyClient import *
from logSys import *
CON_TIMEOUT = 1000#10 seconds

class proxyClientWithTimer(correctHeaderProxyClient):
  def timeoutAction(self):
    pass
  def connectionTimeout(self):
    if self.updated:
      self.updated = False
      from twisted.internet import reactor
      #print('timer called no exp')
      if not self.responseEnd:
        reactor.callLater(CON_TIMEOUT, self.connectionTimeout)
      return
    #print('cacheProxyClient: connection timeout')
    if not self.responseEnd:
      self.timeoutAction()
    
  def handleStatus(self, version, code, message):
    self.updated = True
    correctHeaderProxyClient.handleStatus(self, version, code, message)

  def handleEndHeaders(self):
    self.updated = True
    correctHeaderProxyClient.handleEndHeaders(self)

  def handleHeader(self, key, value):
    self.updated = True
    correctHeaderProxyClient.handleHeader(self, key, value)

  def handleResponsePart(self, data):
    '''
    This function will be called when http response data got.
    Handle the data of the request
    '''
    self.updated = True
    correctHeaderProxyClient.handleResponsePart(self, data)

  def handleResponseEnd(self):
    '''
    This is called when the response data is totally received
    '''
    self.updated = True
    self.responseEnd = True
    printLog('id:',self.smartClientFactory.id,'response end')
    correctHeaderProxyClient.handleResponseEnd(self)

  def connectionMade(self):
    #Connection established
    self.updated = True
    self.responseEnd = False    
    self.connectionTimeout()
    correctHeaderProxyClient.connectionMade(self)
