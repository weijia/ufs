from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass


def startApp(appAndParamList):
    QueueManager.register('getLaunchQ')
    m = QueueManager(address=('localhost', 8810), authkey='abracadabra')
    m.connect()
    launchQ = m.getLaunchQ()
    launchQ.put(appAndParamList)
    return 'done'

    
    
if __name__=="__main__":
    startApp(['D:\\app\\mongodb\\bin\\mongo.bat'])