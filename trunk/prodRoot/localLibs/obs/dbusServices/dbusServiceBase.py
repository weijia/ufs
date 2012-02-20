import dbus.service

################################################################
#Required !!! Override the following interface name
INTERFACE_NAME = 'com.wwjufsdatabase.dbusServiceBaseInterface'


class dbusServiceBase(dbus.service.Object):
    def __init__(self, sessionBus, objectPath, appConfigDictInst = None):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        self.appConfigDictInst = appConfigDictInst
    
    #The following function declaration is just a sample of dbus method
    '''
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def register(self, taskName):
        if (self.taskList.has_key(taskName)) and (self.taskList[taskName]["status"] ==
                "started"):
            return 'Already registered'
        else:
            self.taskList[taskName] = {"status":"started"}
        return 'Task created'
    '''
    pass
    
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='s')
    def exitService(self):
        '''
        mainloop = gobject.MainLoop()
        mainloop.quit()
        '''
        try:
            self.exitServiceCallback()
        except:
            import traceback
            traceback.print_exc()
        print 'exitService called'
        self.loop.quit()
        return 'quitting'


    def setLoop(self, loop):
        self.loop = loop
        
    def getState(self):
        return self.configDictInst