

class taskBaseInterface:
    '''
    Task manager will start a task at the proper time and the task is responsible to update the states for itself in the state database
    '''
    def __init__(self, taskId):
        pass
    def run(self):
        pass
        
import libs.localDb.dictShoveDb as dictShoveDb

        
class taskBase:
    def __init__(self, taskId):
        self.taskInfoDb = dictShoveDb.getListDbLocal('taskInfo')
        self.taskId = taskId
    '''
    A task object will be initialized with an unique ID. And all info for the running task was identified by this ID
    '''
    def runWithoutException(self):
        #Update task database to indicate the task is started
        self.setTaskStart()
        try:
            self.run()
        except:
            print 'exception occurs'
        #Update task database to indicate the task is done
        self.setTaskEnd()
        
    def setTaskStart(self):
        self.taskInfoDb[self.taskId+'.state'] = 'start'
    def setTaskEnd(self):
        self.taskInfoDb[self.taskId+'.state'] = 'end'