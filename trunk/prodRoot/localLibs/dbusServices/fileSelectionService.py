import dbus.service
import dbusServiceBase
import localLibSys
import localLibs.windows.changeNotifyThread as changeNotifyThread
import localLibs.logWin.fileTools as fileTools

################################################################
#Required !!! Override the following interface name
INTERFACE_NAME = 'com.wwjufsdatabase.dirMonitorService'
BUS_NAME_NAME = 'com.wwjufsdatabase.appStarterService'


class changeNotifyOnDbusThread(changeNotifyThread.changeNotifyThread):
    def __init__ ( self, path):
        changeNotifyThread.changeNotifyThread.__init__ ( self, path)

    def callback(self, monitoringPath, file, action):
        bus = dbus.SessionBus()
        proxy = bus.get_object(BUS_NAME_NAME,
                               '/dirMonitor')
        #print 'callback called:', monitoringPath, file, action
        proxy.simpleNotify(monitoringPath, file, action, dbus_interface = INTERFACE_NAME)


class dirMonitorService(dbusServiceBase.dbusServiceBase):
    def __init__(self, sessionBus, objectPath, configDictInst = None):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        self.notifyThreads = {}
        if configDictInst is None:
            self.configDictInst = {"monitoring":{}}
        else:
            self.configDictInst = configDictInst
        self.changedFiles = []
        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='ss', out_signature='s')
    def register(self, dir2Monitor, callbackAppAndParam):
        if (self.configDictInst["monitoring"].has_key(dir2Monitor)):
            if (self.configDictInst["monitoring"][dir2Monitor] == callbackAppAndParam):
                return "Already registered"
            else:
                #Already registered but not the same application
                self.configDictInst["monitoring"][dir2Monitor].append(callbackAppAndParam)
        else:
            self.configDictInst["monitoring"][dir2Monitor] = [callbackAppAndParam]
        
        if self.notifyThreads.has_key(dir2Monitor):
            return "OK"
        #newThread = changeNotifyOnDbusThread(dir2Monitor)
        #newThread.start()
        #self.notifyThreads[dir2Monitor] = newThread
        pa = fileTools.findFileInProduct('dirMonitor.py')
        import appStarterForDbusTest
        ru = [pa, '-p', "%s"%dir2Monitor]
        print ru
        appStarterForDbusTest.startAppFromDbus(ru)
        return "OK"
        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='sss', out_signature='s')
    def simpleNotify(self, monitoringPath, file, action):
        print monitoringPath, file, action
        self.changedFiles.append('%s, %s, %s'%(monitoringPath, file, action))
        return "OK"

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='as')
    def getChangedFiles(self):
        #print monitoringPath, file, action
        return self.changedFiles
        
        
        
def getServiceObj(sessionBus, objectPath, configDictInst):
    return dirMonitorService(sessionBus, objectPath, configDictInst)