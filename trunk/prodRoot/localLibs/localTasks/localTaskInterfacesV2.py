import dbus
import dbus.exceptions
import time

class localTaskInterface:
    def __init__(self, taskName):
        pass
    def process(self):
        '''
        Callback that sub-class should do processing in this method
        '''
        pass

    def saveState(self):
        '''
        Callback that sub-class should save state in this method
        '''
        print 'status saved.'
        
class localTaskBase(localTaskInterface):
    def __init__(self, taskName):
        self.bus = dbus.SessionBus()
        self.proxy = self.bus.get_object('com.wwjufsdatabase.appStarterService',
                               '/taskManager')
        self.taskName = taskName
        self.registerTask()
        self.delayStopCnt = 10
        self.delayCnt = 0
        self.runningFlag = True

    def checkTaskStatus(self):
        '''
        Called by this class, do not call this method in sub-class
        '''
        status = self.proxy.checkTaskStatus(self.taskName,
                dbus_interface = "com.wwjufsdatabase.taskManagerInterface")
        print status
        if 'running' == status:
            return True
        else:
            return False
    def delayRunning(self):
        self.delayCnt += 1
        self.delayCnt = self.delayCnt % self.delayStopCnt
        if self.delayCnt == 0:
             self.runningFlag = self.checkTaskStatus()
        return self.runningFlag
        
    def registerTask(self):
        '''
        Called by this class, do not call this method in sub-class
        Called to register to task manager
        '''
        self.proxy.register(self.taskName)
        
    def run(self):
        cnt = 0
        running = True
        while running:
            completed = self.process()
            time.sleep(1)
            print 'round: %d'%cnt
            cnt += 1
            try:
                running = self.checkTaskStatus()
            except dbus.exceptions.DBusException:
                pass
            if completed:
                break
        self.saveState()
        
if __name__ == '__main__':
    t = localTaskBase('test')
    t.run()