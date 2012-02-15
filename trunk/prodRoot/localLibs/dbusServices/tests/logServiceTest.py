import dbus.service
import dbus

BUS_NAME_NAME = 'com.wwjufsdatabase.logService'
INTERFACE_NAME = 'com.wwjufsdatabase.logService'

def logStr(l):
    bus = dbus.SessionBus()
    proxy = bus.get_object(BUS_NAME_NAME,
                           '/service')
    print proxy.logStr(l, dbus_interface = INTERFACE_NAME)

        
if __name__ == '__main__':
    logStr('hello world')