import libSys
from libs.ufsDb.ufsDbBaseInterface import ufsSimpleDbBaseInterface
import sys
import urllib

import libs.html.serverResponseParser

storageScriptRelativePath = 'http://localhost:9901/apps/ufsDb/storeData.py'
#storageScriptRelativePath = 'http://localhost:9901/apps/test/testParam.py'

class ufsStorageClient(ufsSimpleDbBaseInterface):
  def __init__(self, user, dbName):
    self.dbName = dbName
    self.user = user
    self.transaction = []
    self.flush = True
  # def add(self, objId, key, value, createapp = sys.argv[0]):
    # self.transaction.append('add?dbName=%s&uuid=%s&key=%s&value=%s&app=%s'%(urllib.quote(self.dbName), urllib.quote(str(objId)),urllib.quote(key), urllib.quote(value), urllib.quote(createapp)))
    # if self.flush:
      # self.commit()
  # def getAttr(self, objId, k):
    # pass
  # def update(self, objId, key, value, newValue):
    # pass
  # def getObjIdList(self, key, value, offset = 0, limit = 20):
    # pass
  # def run_in_transaction(self, f):
    # pass
  def storeData(self, key, data, createapp = sys.argv[0]):
    self.transaction.append('add?dbName=%s&key=%s&data=%s&app=%s'%(urllib.quote(self.dbName), urllib.quote(str(key)),urllib.quote(data), urllib.quote(createapp)))
    if self.flush:
      self.commit()
  # def getData(self, key)
    # pass
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

