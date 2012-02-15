import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import dbus.mainloop.glib
import dbusServices.taskManager as taskManager
import fileTools
import subprocess
from dbus.mainloop.glib import threads_init
import dbus.exceptions
#import localLibSys
#import localLibs.logWin.dbusServices.dirMonitorService as dirMonitorService

CREATE_NO_WINDOW = 0x8000000

class appStarter(dbus.service.Object):
    
    @dbus.service.method(dbus_interface='com.wwjufsdatabase.appStarterInterface',
                         in_signature='as', out_signature='s')
    def StringifyVariant(self, strList):
        return ','.join(strList)
    
    @dbus.service.method(dbus_interface='com.wwjufsdatabase.appStarterInterface',
                         in_signature='as', out_signature='s')
    def startApp(self, dbusArrayAppAndParamList):
        print 'start app called'
        appAndParamList = []
        for i in dbusArrayAppAndParamList:
            appAndParamList.append(str(i))
        self.target.addAppToIdleRunner(appAndParamList)
        print 'calling app done'
        return 'done'
        
    @dbus.service.method(dbus_interface='com.wwjufsdatabase.appStarterInterface',
                         in_signature='', out_signature='s')
    def exitService(self):
        '''
        mainloop = gobject.MainLoop()
        mainloop.quit()
        '''
        print 'exitService called'
        self.loop.quit()
        return 'quitting'

    def setTarget(self, target):
        self.target = target
    def setLoop(self, loop):
        self.loop = loop
        

def startAppRunnerService(target = None):
    ########################
    #Start dbus deamon first
    ########################
    dbusAppName = "dbus-daemon.exe"
    dbusAppPath = fileTools.findFileInProduct(dbusAppName)
    processObj = None
    if not (dbusAppPath is None):
        print 'launching dbus daemon'
        processObj = subprocess.Popen([dbusAppPath, "--config-file=session.conf"],
                                        creationflags = CREATE_NO_WINDOW)
    ########################
    threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.wwjufsdatabase.appStarterService", session_bus)
    mainloop = gobject.MainLoop()
    
    ############################
    #Start app starter service
    ############################
    #Set message target so start app message can be sent to the GTK desktop application. And the GTK desktop
    #application will start the real application and add entry to task bar icon menu.
    object = appStarter(session_bus, '/appStarter')
    object.setTarget(target)
    #Set the mainloop obj so app starter service provides 
    object.setLoop(mainloop)
    
    ############################
    #Start task manager service
    ############################
    taskManagerObj = taskManager.taskManagerService(session_bus, '/taskManager')    
    #Only appStarter need to take control on stop the bus message loop
    #taskManagerObj.setLoop(mainloop)
    
    ############################
    #Start task manager service
    ############################
    #dirMon = dirMonitorService.dirMonitorService(session_bus, '/dirMonitor')

    ############################
    #Start main message loop for DBus services
    ############################
    mainloop.run()
    '''
    if not (processObj is None):
        print 'processing:', processObj.pid, int(processObj._handle)
        processManager.killChildProcessTree(processObj.pid)
        win32api.TerminateProcess(int(processObj._handle), -1)
    '''
    print 'quitting mainloop.run()'

def stopAllService():
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object('com.wwjufsdatabase.appStarterService',
                             '/appStarter')
        print 'calling quit all'
        print proxy.exitService()
    except:# dbus.exceptions.DbusException:
        print 'calling stopAllService with exception'

if __name__ == "__main__":
    startAppRunnerService()
