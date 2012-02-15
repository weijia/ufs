from ufsDbBaseInterface import *
import sys

class ufsSimpleDbBase(ufsSimpleDbBaseInterface):
  def __init__(self, tokenDb, entryDb, valueDb = None):
    self.tokenDb = tokenDb
    self.entryDb = entryDb
    if valueDb is None:
      self.valueDb = tokenDb
    else:
      self.valueDb = valueDb
  def add(self, objId, key, value, createapp = sys.argv[0]):
    k = self.tokenDb.getId(key)
    v = self.valueDb.getId(value)
    self.entryDb.add(objId, k, v, createapp)
  def delete(self, objId, key, value):
    k = self.tokenDb.getId(key)
    v = self.valueDb.getId(value)
    self.entryDb.delete(objId, k, v)

  def update(self, objId, key, value, newValue, createapp = sys.argv[0]):
    #print 'ufsSimpleDbBase:',key, value
    k = self.tokenDb.getId(key)
    v = self.valueDb.getId(value)
    nv = self.tokenDb.getId(newValue)
    self.entryDb.update(objId, k, v, nv, createapp)
  def getAttr(self, objId, key):
    k = self.tokenDb.getId(key)
    v = self.entryDb.getAttr(objId, k)
    #print 'obj id is:',objId,'getting key:',k, 'got value id', v
    if v is None:
      return None
    return self.tokenDb.get(v)
  def getAttrList(self, objId, key, offset = 0, limit = 20):
    k = self.tokenDb.getId(key)
    vl = self.entryDb.getAttrList(objId, k, offset, limit)
    #print 'obj id is:',objId,'getting key:',k, 'got value id', vl
    res = []
    #res = [unicode(str(offset)),unicode(str(limit))]
    for i in vl:
      #print 'valueid:',i
      j = self.valueDb.get(i)
      if j is None:
        #raise 'token not defined'
        pass
      else:
        res.append(j)
    #raise "Returned value length:%d"%len(res)
    return res
    
  def getObjIdList(self, key, value, offset = 0, limit = 20):
    k = self.tokenDb.getId(key)
    v = self.valueDb.getId(value)
    #print k,v
    return self.entryDb.getObjIdList(k, v, offset, limit)


class ufsDbBase(ufsSimpleDbBase, ufsDbBaseInterface):#Here the first base class's method will first be selected as this class's method.
  pass
