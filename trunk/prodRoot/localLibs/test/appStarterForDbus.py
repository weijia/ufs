import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject



class appStarter(dbus.service.Object):
    @dbus.service.method(dbus_interface='com.appStarter.appStarter',
                         in_signature='as', out_signature='s')
    def StringifyVariant(self, strList):
        return ','.join(strList)


def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.appStarter.appStarter", session_bus)
    object = appStarter(session_bus, '/com/appStarter/appStarter')

    mainloop = gobject.MainLoop()
    mainloop.run()


if __name__ == "__main__":
    main()
