import dbus.service
import dbus

BUS_NAME_NAME = 'com.wwjufsdatabase.appStarterService'
INTERFACE_NAME = 'com.wwjufsdatabase.dirMonitorService'

def monitorFromDbus(pathAndParam):
        bus = dbus.SessionBus()
        proxy = bus.get_object(BUS_NAME_NAME,
                               '/dirMonitor')
        print proxy.getChangedFiles(dbus_interface = INTERFACE_NAME)

        
if __name__ == '__main__':
    monitorFromDbus('D:\\oldmachine\\sys\\purple')