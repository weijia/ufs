import libSys
from libs.ufsDb.ufsDbBaseInterface import ufsSimpleDbBaseInterface
import sys
import urllib

import libs.html.serverResponseParser

storageScriptRelativePath = 'http://localhost:9901/apps/ufsDb/storeRecords.py'
#storageScriptRelativePath = 'http://localhost:9901/apps/test/testParam.py'

class ufsSimpleDbBaseClient(ufsSimpleDbBaseInterface):
  def __init__(self, user, dbName):
    self.dbName = dbName
    self.user = user
    self.transaction = []
    self.flush = False
  def add(self, objId, key, value, createapp = sys.argv[0]):
    self.transaction.append('add?dbName=%s&uuid=%s&key=%s&value=%s&app=%s'%(urllib.quote(self.dbName), urllib.quote(str(objId)),urllib.quote(key), urllib.quote(value), urllib.quote(createapp)))
    if self.flush:
      self.commit()


  def commit(self):
    e = urllib.urlencode({'operationData':'\n'.join(self.transaction), 'sessionId': self.user.getSessionId()})
    print e
    if True:
      f = urllib.urlopen(storageScriptRelativePath, e, proxies={})
    else:
      print storageScriptRelativePath+'?'+e
      f = urllib.urlopen(storageScriptRelativePath+'?'+e, proxies={})
      
    p = libs.html.serverResponseParser.serverResponseParser()
    print 'returned value-------------------------------'
    l = p.parseValueList(f)
    print l

