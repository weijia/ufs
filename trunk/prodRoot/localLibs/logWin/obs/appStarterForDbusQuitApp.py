import dbus


def stopService():
    bus = dbus.SessionBus()
    proxy = bus.get_object('com.wwjufsdatabase.appStarterService',
                           '/appStarter')
    # proxy is a dbus.proxies.ProxyObject
    print proxy.exitService()

    
    
if __name__ == '__main__':
    stopService()