import dbus
bus = dbus.SessionBus()
proxy = bus.get_object('com.appStarter.appStarter',
                       '/com/appStarter/appStarter')
# proxy is a dbus.proxies.ProxyObject
print proxy.StringifyVariant(['good','bad'])