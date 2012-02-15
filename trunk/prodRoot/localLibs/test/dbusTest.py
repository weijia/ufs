import dbus
import dbus.service

class Example(dbus.service.Object):
    def __init__(self, object_path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), object_path)

    @dbus.service.signal(dbus_interface='com.example.Sample',
                         signature='us')
    def NumberOfBottlesChanged(self, number, contents):
        print "%d bottles of %s on the wall" % (number, contents)

if True:
    '''
    Without the following codes, we'll receive the following error:
    RuntimeError: To make asynchronous calls, receive signals or export objects, D-B
us connections must be attached to a main loop by passing mainloop=... to the co
nstructor or calling dbus.set_default_main_loop(...)
    '''
    from dbus.mainloop.glib import DBusGMainLoop

    dbus_loop = DBusGMainLoop()

    bus = dbus.SessionBus(mainloop=dbus_loop)
        
        
e = Example('/bottle_counter')
e.NumberOfBottlesChanged(100, 'beer')