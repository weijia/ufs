import dbus.service
import dbus

#BUS_NAME_NAME = 'com.wwjufsdatabase.appStarterService'
BUS_NAME_NAME = 'com.wwjufsdatabase.dirMonitorService'
INTERFACE_NAME = 'com.wwjufsdatabase.dirMonitorService'

def monitorFromDbus(pathAndParam):
        bus = dbus.SessionBus()
        proxy = bus.get_object(BUS_NAME_NAME,
                               '/dirMonitor')
        print proxy.simpleNotify('monitoring','file','action',dbus_interface = INTERFACE_NAME)

        
if __name__ == '__main__':
    monitorFromDbus('D:\\oldmachine\\sys\\purple')