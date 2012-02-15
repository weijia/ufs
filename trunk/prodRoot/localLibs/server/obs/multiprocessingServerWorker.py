import localLibSys
import libs.ufsDb.dbSys as dbSys

from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass


def processor(reqQ, resQ):
    gDbDict = {}
    while True:
        r = reqQ.get()
        reqType, key, dbName, value = r
        print 'get req for %s'%dbName.encode('gb2312', 'replace')
        try:
            db = gDbDict[dbName]
        except KeyError:
            db = dbSys.dbSysSmart().getDb(dbName)
            gDbDict[dbName] = db

        if '0' == reqType:
            #End req
            return
        if '1' == reqType:
            #Query
            try:
                value = db[key]
                if type(value) == list:
                    v = u','.join(value)
                else:
                    v = value
                resQ.put((db[key], r))
                print 'find %s = %s'%(key.encode('gb2312', 'replace'), v.encode('gb2312', 'replace'))
            except KeyError:
                print '%s not exist'%key.encode('gb2312', 'replace')
                resQ.put(([], r))
        if '2' == reqType:
            if type(value) == list:
                v = u','.join(value)
            else:
                v = value
            print 'set:%s = %s'%(key.encode('gb2312', 'replace'),v.encode('gb2312', 'replace'))
            db[key] = value

'''            
import subprocess
import sys
# some code here
#pid = subprocess.Popen([sys.executable, "multiprocessingServer.py"]) # call subprocess
# some more code here
DETACHED_PROCESS = 0x00000008

pid = subprocess.Popen([sys.executable, "multiprocessingServer.py"],
                       creationflags=DETACHED_PROCESS).pid
'''
QueueManager.register('getReqQ')
QueueManager.register('getResQ')
m = QueueManager(address=('localhost', 8809), authkey='abracadabra')
m.connect()
reqQ = m.getReqQ()
resQ = m.getResQ()
processor(reqQ, resQ)


