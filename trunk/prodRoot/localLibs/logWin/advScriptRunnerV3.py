import scriptRunnerV2 as scriptRunner
import gobject
import threading
import gtk

class advScriptRunner(scriptRunner.dropRunWnd):
    def startScriptRunnerApp(self, launchServiceThreadClass):
        scriptRunner.dropRunWnd.startScriptRunnerApp(self)
        self.serverThread = launchServiceThreadClass(self)
        self.serverThread.start()
    def quitAll(self):
        self.serverThread.stopAllTasks()
        self.serverThread.stop()

        
    def addAppToIdleRunner(self, param):
        print 'callback called'
        gobject.idle_add(self.lauchServerLaunch, param)
        import time
        time.sleep(0.1)

    def lauchServerLaunch(self, param):
        self.startAppWithParam(param)
    def close_application(self, widget):
        self.quitAll()
        scriptRunner.dropRunWnd.close_application(self, widget)

def startApplicationsNoReturn(l, launchServiceThreadClass):
    '''
    from dbus.mainloop.glib import threads_init
    threads_init()
    '''
    d = advScriptRunner()
    d.initialApps = l
    d.startScriptRunnerApp(launchServiceThreadClass)
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    print 'after gtk.gdk.threads_leave()'
    d.quitAll()
    print 'final quit'
    import sys
    sys.exit()
    return 0
    
  
def main():
    startApplicationsNoReturn([])

if __name__ == "__main__":
    main()
