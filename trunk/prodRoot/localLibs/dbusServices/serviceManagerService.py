import localLibSys
import dbus
import dbusServiceBase
import localLibs.collection.objectDatabase as objectDatabase

#applicationStorageUuid = u"xxxx-xxxx-x"


class serviceManagerService(dbusServiceBase.dbusServiceBase):
    def initTaskList(self):
        if self.appConfigDictInst.has_key("taskList"):
            self.appConfigDictInst["taskList"] = {}
        self.taskList = self.appConfigDictInst["taskList"]
        
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
        self.initTaskList()
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
        self.initTaskList()
        r = 'task list:'
        for i in self.taskList:
            o = 'task:%s, status:%s;'%(i, self.taskList[i]["status"])
            r += o
        return r
        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def stopTask(self, taskName):
        self.initTaskList()
        if not self.taskList.has_key(taskName):
            return 'Not registered'
        else:
            self.taskList[taskName] = {"status":"stopped"}
            return 'task stopped'
        return 'Task created'

