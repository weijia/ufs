import dbus


def startAppFromDbus(pathAndParam):
    bus = dbus.SessionBus()
    proxy = bus.get_object('com.wwjufsdatabase.appStarterService',
                           '/appStarter')
    '''
    # proxy is a dbus.proxies.ProxyObject
    print proxy.StringifyVariant(['good','bad'], 
        dbus_interface = "com.wwjufsdatabase.appStarterInterface")
    print proxy.startApp(['D:\\apps\\mongodb\\mongodb-win32-i386-1.6.5\\bin\\startMongoDb.bat'],
        dbus_interface = "com.wwjufsdatabase.appStarterInterface")
    '''
    print proxy.startApp(pathAndParam,
        dbus_interface = "com.wwjufsdatabase.appStarterInterface")
        
if __name__ == '__main__':
    startAppFromDbus(['D:\\apps\\mongodb\\mongodb-win32-i386-1.6.5\\bin\\startMongoDb.bat'])