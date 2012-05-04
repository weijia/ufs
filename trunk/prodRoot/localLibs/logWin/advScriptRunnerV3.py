import scriptRunnerV2 as scriptRunner
import gobject
#import threading
import gtk
import time

class advScriptRunner(scriptRunner.dropRunWnd):
    def startScriptRunnerApp(self, launchServiceThreadClass):
        scriptRunner.dropRunWnd.startScriptRunnerApp(self)
        self.serverThread = launchServiceThreadClass(self)
        self.serverThread.start()
    def quitAllXmlRpcServer(self):
        self.serverThread.send_stop_to_all_registered_xml_rpc_server()
        self.serverThread.stop()

        
    def addAppToIdleRunner(self, param):
        print 'callback called'
        gobject.idle_add(self.lauchServerLaunch, param)
        #import time
        time.sleep(0.1)

    def lauchServerLaunch(self, param):
        self.create_console_wnd_for_app(param)
    def close_application(self, widget):
        '''
        This is called when task bar icon menu "exit" was clicked. It is the very beginning of the quit process.
        '''
        self.quitAllXmlRpcServer()
        time.sleep(5)
        scriptRunner.dropRunWnd.close_application(self, widget)

def startApplicationsNoReturn(l, launchServiceThreadClass):
    d = advScriptRunner()
    d.initialApps = l
    d.startScriptRunnerApp(launchServiceThreadClass)
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    print 'after gtk.gdk.threads_leave()'
    #d.quitAll()
    print 'final quit'
    import sys
    sys.exit()
    return 0
    
  
def main():
    startApplicationsNoReturn([])

if __name__ == "__main__":
    main()
