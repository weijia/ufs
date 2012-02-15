#import mimetypes
from url2name import *
from twisted.web import proxy
from logSys import *
from dummyProxyClientFactory import *
gTestCacheServer = False
from correctHeaderProxyClient import *
from tools import *

import localLibSys
from localLibs.logSys.logSys import *


class cacheClient:
  def __init__(self, cachedPath, info):
    self.cachedPath = cachedPath
    self.info = info
    ncl(self.info['headers'])
  def sendResponse(self, client):
    try:
      #Try to open file first
      self.filenameExt = genExtFromHeaders(self.info['headers'])
      cl(self.filenameExt)
      data = open(os.path.join(self.cachedPath, 'content'+ self.filenameExt), 'rb').read()
      #send status
      print self.info['status']['version'],\
        self.info['status']['code'],\
        self.info['status']['message']
      try:
        if int(self.info['code']) == 206:
          client.handleStatus('HTTP/1.1', '200', 'OK')
        else:
          client.handleStatus(self.info['status']['version'],
            self.info['status']['code'],
            self.info['status']['message'])
      except KeyError:
        cl('line 35, info key error',self.info)
      #send headers
      sentHeader = []
      for i in self.info['headersOrdered']:
        if i == 'content-range':
          cl('content-range exist')
          continue
        if i == 'content-length':
          pass
        try:
          sentHeader.index(i)
        except ValueError:
          try:
            formated = formatHeader(i)
            ncl(formated)
            client.handleHeader(formated, self.info['headers'][i])
            sentHeader.append(i)
          except:
            pass
        #print i, self.info['headers'][i]
      print 'header sent----------------'
      client.handleEndHeaders()
      #send response
      client.handleResponsePart(data)
      client.handleResponseEnd()
      print 'sending data---------------'
      print len(data)
      #print 'send content successfully'
      return True
    except IOError:
      print 'can not open ',os.path.join(self.cachedPath, 'content'+ self.filenameExt)
      return False

class cacheClientFactory(proxy.ProxyClientFactory):
    def __init__(self, command, rest, version, headers, data, father):
        self.id = None
        proxy.ProxyClientFactory.__init__(self, command, rest, version, \
            headers, data, father)

    def buildProtocol(self, addr):
        client = proxy.ProxyClientFactory.buildProtocol(self, addr)
        printLog('id:',self.id,'protocol built, cacheProxyClient used')
        client.transport = dummyProxyClientFactoryTransport()
        client.id = self.id
        return client


class cacheManager:
  def __init__(self):
    self.db = Shove('sqlite:///info.sqlite')
    #self.ufsDb = ufsDb('proxyDb')
    self.fileDb = {}
  def checkObjIntegrity(self, info):
    #If testing, always return true
    if gTestCacheServer:
      return True
    print info
    try:
      cl('status: ',info['status']['code'])
      if info['status']['code'] == '404':
        cl('no such domain, no cache')
        return False
    except:
      pass

    if info['parts'].has_key('totalLength'):
      cl('cacheManager, curp:',info['parts']['curPos'],',total: ',info['parts']['totalLength'])
      if int(info['parts']['curPos']) == int(info['parts']['totalLength']):
        print 'all data received, returning true'
        return True
    else:
      print 'no length info',info['headers'],' cur pos:',info['parts']['curPos']
      #Check the file integraty
    return False
  def getCacheClient(self, uri):
    #Check if url is fully cached
    cachedPath = url2dir(uri)
    print 'cachedPath', cachedPath
    try:
      db = open(os.path.join(cachedPath,'objDb.cpickle'),'rb')
      import pickle
      try:
        info = pickle.load(db)
      except EOFError:
        db.close()
        cl('pickle broken, remove the cached one')
        import shutil
        shutil.rmtree(cachedPath)
        return None
      db.close()
      if self.checkObjIntegrity(info):
        #Cached the whole object
        cl('Page cached,  return to client directly')
        return cacheClient(cachedPath, info)
      else:
        #print 'file not downloaded totally, remove it'
        #import shutil
        #shutil.rmtree(cachedPath)
        return None
    except IOError:
        #print 'Can not open info file, it is not cached'
        return None
