#import localLibSys
import win32com.client
import win32api

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

