import dbus.service
import localLibSys
import localLibs.dbusServices.dbusServiceBase as dbusServiceBase

INTERFACE_NAME = 'com.wwjufsdatabase.taskManagerInterface'

class taskManagerService(dbusServiceBase.dbusServiceBase):
    def __init__(self, paramA, paramB):
        dbusServiceBase.dbusServiceBase.__init__(self, paramA, paramB)
        self.taskList = {}


    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def register(self, taskName):
        if (self.taskList.has_key(taskName)) and (self.taskList[taskName]["status"] ==
                "started"):
            return 'Already registered'
        else:
            self.taskList[taskName] = {"status":"started"}
        return 'Task created'
        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def checkTaskStatus(self, taskName):
        if not self.taskList.has_key(taskName):
            return 'Not registered'
        elif self.taskList[taskName]["status"] == 'started':
            return 'running'
        elif self.taskList[taskName]["status"] == 'stopped':
            return 'stopped'
        else:
            return 'unknown state'
            
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='s')
    def getTaskList(self):
        r = 'task list:'
        for i in self.taskList:
            o = 'task:%s, status:%s;'%(i, self.taskList[i]["status"])
            r += o
        return r
        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def stopTask(self, taskName):
        if not self.taskList.has_key(taskName):
            return 'Not registered'
        else:
            self.taskList[taskName] = {"status":"stopped"}
            return 'task stopped'
        return 'Task created'

        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='s')
    def exitService(self):
        return self.exitServiceFunc()