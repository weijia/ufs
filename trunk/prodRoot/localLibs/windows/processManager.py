#import localLibSys
import win32com.client
import win32api

#Codes from http://code.activestate.com/recipes/496767-set-process-priority-in-windows/
def setPriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """
        
    import win32api,win32process,win32con
    
    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])

def findProcessHandle(pid):
    WMI = win32com.client.GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    for process in processes:
        currentPid = process.Properties_('ProcessID').Value
        parent = process.Properties_('ParentProcessId').Value
        handle = process.Properties_('Handle').Value
        #print childPid, parent
        if int(currentPid) == int(pid):
            print 'find handle for pid:%d , is %d'%(int(pid), int(handle))
            return int(handle)
    raise 'no handle for pid found'
    
def terminateProcessByPid(pid):
    WMI = win32com.client.GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    for process in processes:
        currentPid = process.Properties_('ProcessID').Value
        parent = process.Properties_('ParentProcessId').Value
        handle = process.Properties_('Handle').Value
        #print childPid, parent
        if int(currentPid) == int(pid):
            print 'find handle for pid:%d , is %d'%(int(pid), int(handle))
            process.Terminate()
            return
    raise 'no handle for pid found'


def killChildProcessTree(pid, killRoot = False):
    WMI = win32com.client.GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    for process in processes:
        childPid = process.Properties_('ProcessID').Value
        parent = process.Properties_('ParentProcessId').Value
        handle = process.Properties_('Handle').Value
        #print childPid, parent
        if int(parent) == int(pid):
            print '--------------------------------------------match'
            killChildProcessTree(childPid, True)
    if True == killRoot:
        handle = findProcessHandle(int(pid))
        print 'terminating root:', handle
        #win32api.TerminateProcess(handle, -1)
        terminateProcessByPid(pid)

