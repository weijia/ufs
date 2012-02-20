import dbus.service
import dbus

#BUS_NAME_NAME = 'com.wwjufsdatabase.appStarterService'
BUS_NAME_NAME = 'com.wwjufsdatabase.collectionService'
INTERFACE_NAME = 'com.wwjufsdatabase.collectionService'

def monitorFromDbus(path2Monitor, pathAndParam):
        bus = dbus.SessionBus()
        proxy = bus.get_object(BUS_NAME_NAME,
                               '/service')
        proxy.register(path2Monitor, pathAndParam, dbus_interface = INTERFACE_NAME)

        
if __name__ == '__main__':
    monitorFromDbus('D:\\tmp\\fileman\\data\\encZip', "D:\\codes\\mine\\ufs\\prodRoot\\localLibs\\dbusServices\\tests\\archiveTest.py")