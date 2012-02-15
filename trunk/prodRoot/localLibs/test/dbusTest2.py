import dbus
import dbus.service
import dbus.mainloop.glib

'''
code copied from http://www.kissuki.com/2010/09/%E4%BD%BF%E7%94%A8-dbus-python-%E5%BB%BA%E7%AB%8B%E5%8D%95%E5%AE%9E%E4%BE%8B%E8%BF%9B%E7%A8%8B/
'''
class SingleInstanceAppMixin:
    "Single Instance Application"

    def __init__(self, bus_name):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)
        self.bus = dbus.SessionBus()
        try:
            self.bus_name = dbus.service.BusName(bus_name,
                    self.bus, allow_replacement = False, replace_existing = False, do_not_queue = True)
        except dbus.exceptions.NameExistsException:
            print "Another instance is already running."
            self.on_instance_exists()

    def on_instance_exists(self):
        """
        This method is called when an instance of the program already
        exists. It may be overwritten by subclasses.
        """
        print 'instance exists'
        import sys
        sys.exit(0)
        
        
import time
def main():
    #Here, must assign the appMixin obj to a variable, so it will not be 
    #destructed before another application was created.
    p = SingleInstanceAppMixin('great.time')
    time.sleep(100000)

if __name__ == "__main__":
    main()
