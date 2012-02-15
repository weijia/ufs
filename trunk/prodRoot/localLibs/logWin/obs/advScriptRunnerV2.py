import gobject
import threading
import gtk
import appStarterForDbusV2 as appStarterForDbus
import advScriptRunnerV3 as advScriptRunner


class scriptLauncherDbusTherd(threading.Thread):
    def __init__(self, target):
        self.target = target
        threading.Thread.__init__(self)
    def run(self):
        #Connect to server
        appStarterForDbus.startAppRunnerService(self.target)
        print 'quit running appStarterForDbus.startAppRunnerService(self.target)'
    def stop(self):
        appStarterForDbus.stopAllService()

def startApplicationsNoReturn(l):
    '''
    from dbus.mainloop.glib import threads_init
    threads_init()
    '''
    d = advScriptRunner.advScriptRunner()
    d.initialApps = l
    d.startScriptRunnerApp(scriptLauncherDbusTherd)
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    print 'after gtk.gdk.threads_leave()'
    d.quitAll()
    print 'final quit'
    return 0

  
def main():
    startApplicationsNoReturn([])

if __name__ == "__main__":
    main()
