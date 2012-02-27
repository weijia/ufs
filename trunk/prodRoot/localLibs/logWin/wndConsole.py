import threading
import subprocess
import os
import localLibSys
import localLibs.windows.processManager as processManager
CREATE_NO_WINDOW = 0x8000000


class taskConsoleThread(threading.Thread):
    def __init__(self, target, fileD, appname = 'unknown'):
        self.target = target
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.fileD = fileD
        self.appname = appname
    def run(self):
        #print 'running'
        while not self.quitFlag:
            #print 'before readline'
            err = self.fileD.readline()
            #print 'after readline'
            if err == '':
                #print 'err is empty'
                self.quit()
            if err is None:
                self.quit()
                #print 'quit'
                break
            #print 'got output:',err
            self.target.updateViewCallback(err)
        print 'quitting run: ',self.appname
    def quit(self):
        self.quitFlag = True


        
class wndConsole:
    def __init__(self):
        self.threadList = []
        self.pList = []
    def runConsoleApp(self, target, cwd = 'D:\\code\\python\\developing\\ufs', progAndParm = ['D:\\code\\python\\developing\\ufs\\webserver-cgi.py']):
        checkExistPath = progAndParm
        if type(checkExistPath) == list:
            checkExistPath = checkExistPath[0]
            if not os.path.exists(checkExistPath):
                #Do not execute if the file does not exist
                return
        self.cwd = cwd
        self.progAndParm = progAndParm
        #print target
        #print '-------------------------',progAndParm
        #print cwd
        #self.prog = ['D:\\cygwin\\bin\\ls.exe','-l']
        ext = os.path.splitext(checkExistPath)[1]
        print 'ext is:', ext
        if ".py" == ext:
            pythonWinPathList = ['e:/python27/pythonw.exe','d:/python25/pythonw.exe','c:/python27/pythonw.exe', 'c:/python26/pythonw.exe', 'c:/python25/pythonw.exe']
            for i in pythonWinPathList:
                if os.path.exists(i):
                    targetPythonExePath = i
                    break
            self.prog = [targetPythonExePath,'-u']
            self.prog.extend(progAndParm)#Param 2 is the app
        else:
            self.prog = []
            self.prog.extend(progAndParm)
        #print '-------------------------',self.prog
        #return
        '''
        #self.prog.append('D:\\code\\python\\webserver-cgi.py')
        #self.cwd = 'D:\\code\\python\\'
        #self.cwd = sys.argv[1]#Param 1 is the cwd
        
        import os
        self.cwd = os.getcwd()
        '''
        #print self.prog
        #self.SetTitle(progAndParm[0])
        if True:#try:
            #print self.prog
            p = subprocess.Popen(self.prog, cwd = self.cwd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize=0, creationflags = CREATE_NO_WINDOW)
            self.pList.append(p)
            #print 'taskid:%d, pid:%d'%(int(p._handle), int(p.pid))
            thr1 = taskConsoleThread(target, p.stdout, progAndParm[0])
            thr1.start()
            self.threadList.append(thr1)
            thr2 = taskConsoleThread(target, p.stderr, progAndParm[0])
            thr2.start()
            self.threadList.append(thr2)
            #print 'launch ok'
        else:#except:
            print 'launch exception'
        #self.appStarted = True
    def close(self):
        import win32api
        '''
        #Following codes got from http://mail.python.org/pipermail/python-win32/2009-September/009543.html
        import win32com.client
        WMI = win32com.client.GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        for process in processes:
            pid = process.Properties_('ProcessID').Value
            parent = process.Properties_('ParentProcessId')
            print 'process id and parent:', pid, parent
            #Kill all child process
            for process in processes:
                pid = process.Properties_('ProcessID').Value
                parent = process.Properties_('ParentProcessId')
                handle = process.Properties_('Handle')
                print pid, parent, handle
                print 'pid is:',i.pid
                if parent == i.pid:
                    pass
            print 'terminating: %d'%int(i._handle)
            try:
                print win32api.TerminateProcess(int(i._handle), -1)
            except:
                print 'TerminatProcess error'
        '''
        for i in self.pList:
            print 'processing:', i.pid, int(i._handle)
            processManager.killChildProcessTree(i.pid)
            win32api.TerminateProcess(int(i._handle), -1)
    
        for i in self.threadList:
            i.quit()
