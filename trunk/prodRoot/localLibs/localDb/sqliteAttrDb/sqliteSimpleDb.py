import localLibSys
import libs.ufsDb.ufsDbBaseInterface as ufsDbBaseInterface
import valueDbStorage

class ufsSimpleDbBase(ufsDbBaseInterface):
    # def __init__(self, tokenDb, entryDb):
    # pass
    def add(self, objId, key, value, createapp):
        valueDbStorage
    def getAttr(self, objId, k):
        pass
    def update(self, objId, key, value, newValue):
        pass
    def getObjIdList(self, key, value, offset = 0, limit = 20):
        pass
    def run_in_transaction(self, f):
        pass
