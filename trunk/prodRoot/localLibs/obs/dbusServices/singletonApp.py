#Codes from http://www.kissuki.com/2010/09/%e4%bd%bf%e7%94%a8-dbus-python-%e5%bb%ba%e7%ab%8b%e5%8d%95%e5%ae%9e%e4%be%8b%e8%bf%9b%e7%a8%8b/
import dbus
import dbus.service
import dbus.mainloop.glib

class SingleInstanceAppMixin:
    "Single Instance Application"

    def __init__(self, bus_name):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)
        self.bus = dbus.SessionBus()
        try:
            self.bus_name = dbus.service.BusName(bus_name,
                    self.bus, allow_replacement = False, replace_existing = True, do_not_queue = True)
        except dbus.exceptions.NameExistsException:
            print "Another instance is already running."
            self.on_instance_exists()

    def on_instance_exists(self):
        """
        This method is called when an instance of the program already
        exists. It may be overwritten by subclasses.
        """
        import sys
        sys.exit(0)