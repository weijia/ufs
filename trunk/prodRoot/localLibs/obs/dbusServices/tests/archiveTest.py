import dbus.service
import dbus

BUS_NAME_NAME = 'com.wwjufsdatabase.encZipStorageService'
INTERFACE_NAME = 'com.wwjufsdatabase.encZipStorageService'

def monitorFromDbus(pathAndParam):
        bus = dbus.SessionBus()
        proxy = bus.get_object(BUS_NAME_NAME,
                               '/service')
        proxy.register(pathAndParam, "no callback", dbus_interface = INTERFACE_NAME)

        
if __name__ == '__main__':
    monitorFromDbus('D:\\tmp\\fileman', )