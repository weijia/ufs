import libSys
import libs.localDb.dictShoveDb as dictShoveDb

#---------------------------------copied from logWin fileTools
import os
def findFileInProduct(filename):
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        if filename in filenames:
            print 'find file in:',dirpath
            return os.path.join(dirpath, filename)
#---------------------------------copied from logWin fileTools



from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass
import consoleAppLauncher

def startDbWorkerManager():
    QueueManager.register('getLaunchQ')
    QueueManager.register('getResQ')
    m = QueueManager(address=('localhost', 8809), authkey='abracadabra')
    m.connect()
    dbWokerManagerQ = m.getLaunchQ()
    while True:
        dbNameReq = dbWokerManagerQ.get()
        #Start the db worker
        workerName = "dbWorker.py"
        fullPath = findFileInProduct(workerName)
        consoleAppLauncher.launchScript([fullPath, dbNameReq])


