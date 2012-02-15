import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject

from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass


class appStarter(dbus.service.Object):
    
    @dbus.service.method(dbus_interface='com.wwjufsdatabase.appStarterInterface',
                         in_signature='as', out_signature='s')
    def StringifyVariant(self, strList):
        return ','.join(strList)
    
    @dbus.service.method(dbus_interface='com.wwjufsdatabase.appStarterInterface',
                         in_signature='as', out_signature='s')
    def startApp(self, appAndParamList):
        print 'start app called'
        QueueManager.register('getLaunchQ')
        m = QueueManager(address=('localhost', 8809), authkey='abracadabra')
        m.connect()
        launchQ = m.getLaunchQ()
        launchQ.put(appAndParamList)
        return 'done'

        

    def setTarget(self, target):
        self.target = target

        

def startAppRunnerService(target = None):
    from dbus.mainloop.glib import threads_init
    threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.wwjufsdatabase.appStarterService", session_bus)
    object = appStarter(session_bus, '/appStarter')
    object.setTarget(target)
    mainloop = gobject.MainLoop()
    mainloop.run()


if __name__ == "__main__":
    startAppRunnerService()
