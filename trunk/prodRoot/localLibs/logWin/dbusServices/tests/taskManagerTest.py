import dbus


def listTask():
    bus = dbus.SessionBus()
    proxy = bus.get_object('com.wwjufsdatabase.appStarterService',
                           '/taskManager')

    print proxy.getTaskList(dbus_interface = "com.wwjufsdatabase.taskManagerInterface")
        
if __name__ == '__main__':
    listTask()