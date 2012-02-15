import scriptRunnerV2 as scriptRunner
import gobject
import threading
import gtk
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
#import appStarterForDbus

class QueueManager(BaseManager): pass

class serverThread(threading.Thread):
    def run(self):
        queue = Queue()
        QueueManager.register('getLaunchQ', callable=lambda:queue)
        m = QueueManager(address=('localhost', 8910), authkey='abracadabra')
        s = m.get_server()
        s.serve_forever()

class scriptLauncherThread(threading.Thread):
    def __init__(self, target):
        self.target = target
        threading.Thread.__init__(self)
        self.server = serverThread()
        self.server.start()
    def run(self):
        queue = Queue()
        QueueManager.register('getLaunchQ')
        m = QueueManager(address=('localhost', 8910), authkey='abracadabra')
        m.connect()
        launchQ = m.getLaunchQ()
        while True:
            param = launchQ.get()
            print 'Get an item from queue'
            self.target.addAppToIdleRunner(param)
'''
class scriptLauncherDbusTherd(threading.Thread):
    def __init__(self, target):
        self.target = target
        threading.Thread.__init__(self)
    def run(self):
        #Connect to server
        appStarterForDbus.startAppRunnerService(self.target)
'''
class advScriptRunner(scriptRunner.dropRunWnd):
    def startScriptRunnerApp(self):
        scriptRunner.dropRunWnd.startScriptRunnerApp(self)
        #Add listener for launch script
        self.launchThread = scriptLauncherThread(self)
        self.launchThread.start()
        '''
        self.dbusThread = scriptLauncherDbusTherd(self)
        self.dbusThread.start()
        #appStarterForDbus.startAppRunnerService(self)
        '''
        
    def addAppToIdleRunner(self, param):
        #print 'callback called'
        gobject.idle_add(self.lauchServerLaunch, param)
        import time
        time.sleep(0.1)

    def lauchServerLaunch(self, param):
        self.startAppWithParam(param)
    

def startApplicationsNoReturn(l):
    d = advScriptRunner()
    d.initialApps = l
    d.startScriptRunnerApp()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    return 0
    
  
def main():
    startApplicationsNoReturn([])

if __name__ == "__main__":
    main()
