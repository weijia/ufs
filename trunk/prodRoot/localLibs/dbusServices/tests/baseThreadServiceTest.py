import dbus.service
import dbus

#BUS_NAME_NAME = 'com.wwjufsdatabase.appStarterService'
BUS_NAME_NAME = 'com.wwjufsdatabase.baseThreadService'
INTERFACE_NAME = 'com.wwjufsdatabase.baseThreadService'

def monitorFromDbus():
        bus = dbus.SessionBus()
        proxy = bus.get_object(BUS_NAME_NAME,
                               '/service')
        proxy.test()

        
if __name__ == '__main__':
    monitorFromDbus()