import dbus.service

INTERFACE_NAME = 'com.wwjufsdatabase.dbusServiceBaseInterface'

class dbusServiceBase(dbus.service.Object):
    def exitServiceFunc(self):
        '''
        mainloop = gobject.MainLoop()
        mainloop.quit()
        '''
        print 'exitService called'
        self.loop.quit()
        return 'quitting'

    def setLoop(self, loop):
        self.loop = loop
