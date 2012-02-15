import libSys
import libs.localDb.dictShoveDb as dictShoveDb

from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass


def processor(reqQ, resQ):
    gDbDict = {}
    while True:
        reqType, key, dbName, value = reqQ.get()
        print 'get req for %s'%dbName
        try:
            db = gDbDict[dbName]
        except KeyError:
            db = dictShoveDb.getDbV4(dbName)
            gDbDict[dbName] = db

        if '0' == reqType:
            #End req
            return
        if '1' == reqType:
            #Query
            try:
                resQ.put(db[key])
                print 'find %s = %s'%(key, db[key])
            except KeyError:
                print '%s not exist'%key.encode('gb2312', 'replace')
                resQ.put([])
        if '2' == reqType:
            print 'set:%s = %s'%(key.encode('gb2312', 'replace'),value.encode('gb2312', 'replace'))
            db[key] = value


def dbWorker(dbName):
    QueueManager.register('getReqQForDb')
    QueueManager.register('getResQForDb')
    m = QueueManager(address=('localhost', 8809), authkey='abracadabra')
    m.connect()
    reqQ = m.getReqQForDb(dbName)
    resQ = m.getResQForDb(dbName)
    processor(reqQ, resQ)

def main():
    dbName = sys.argv[1]
    dbWorker(dbName)

    
if __name__ == "__main__":
    main()
