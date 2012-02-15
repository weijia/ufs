from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass


class keyValueReq:
    def __init__(self, op, key, dbName, value = None):
        self.op = op
        self.key = key
        self.dbName = dbName
        self.value = value
class syncError: pass
class sharedDb:
    def __init__(self):
        QueueManager.register('getReqQ')
        QueueManager.register('getResQ')
        
        m = QueueManager(address=('localhost', 8809), authkey='abracadabra')
        m.connect()
        self.reqQ = m.getReqQ()
        self.resQ = m.getResQ()
        
    def get(self, key, dbName):
        while not self.resQ.empty():
            self.resQ.get()
        originalR = ('1', key, dbName, None)
        self.reqQ.put(originalR)
        v, r = self.resQ.get()
        if r != originalR:
            raise syncError
        return v
        
    def set(self, key, value, dbName):
        self.reqQ.put(('2', key, dbName, value))

    def delete(self, key, dbName):
        self.reqQ.put(('3', key, dbName, None))


        
if __name__ == '__main__':
    db = sharedDb()
    db.set(u"hello", u"201012051538goodbye", u"testing")
    db.get(u"hello", u"testing")