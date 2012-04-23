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
    normal_priority_tasks = ["webserver-cgi", "startBeanstalkd.bat", "mongodb.bat", "cherrypyServerV3", "monitorServiceV2"]
    def __init__(self):
        self.threadList = []
        self.pList = []
    def runConsoleApp(self, target, cwd = 'D:\\code\\python\\developing\\ufs', progAndParam = ['D:\\code\\python\\developing\\ufs\\webserver-cgi.py']):
        checkExistPath = progAndParam
        if type(checkExistPath) == list:
            checkExistPath = checkExistPath[0]
            if not os.path.exists(checkExistPath):
                #Do not execute if the file does not exist
                return
        self.cwd = cwd
        self.progAndParm = progAndParam
        #print target
        #print '-------------------------',progAndParam
        #print cwd
        #self.prog = ['D:\\cygwin\\bin\\ls.exe','-l']
        ext = os.path.splitext(checkExistPath)[1]
        #print 'ext is:', ext
        if ".py" == ext:
            pythonWinPathList = ['c:/Python27/pythonw.exe','e:/python27/pythonw.exe','d:/python25/pythonw.exe',
                                 'c:/python27/pythonw.exe', 'c:/python26/pythonw.exe', 'c:/python25/pythonw.exe']
            for i in pythonWinPathList:
                if os.path.exists(i):
                    targetPythonExePath = i
                    break
            self.prog = [targetPythonExePath,'-u']
            self.prog.extend(progAndParam)#Param 2 is the app
        else:
            self.prog = []
            self.prog.extend(progAndParam)

        #print self.prog
        #self.SetTitle(progAndParam[0])
        if True:#try:
            #print self.prog
            p = subprocess.Popen(self.prog, cwd = self.cwd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize=0, creationflags = CREATE_NO_WINDOW)
            self.pList.append(p)

            find_flag = False
            for z in self.normal_priority_tasks:
                if progAndParam[0].find(z) != -1:
                    #Need normal priority for this app
                    find_flag = True
            if not find_flag:
                processManager.setPriority(p.pid, 1)
                #print "setting pid: %d, %s to below normal priority"%(p.pid, progAndParam[0])
            else:
                #print "pid: %d, %s use normal priority"%(p.pid, progAndParam[0])
                pass
            #print 'taskid:%d, pid:%d'%(int(p._handle), int(p.pid))
            thr1 = taskConsoleThread(target, p.stdout, progAndParam[0])
            thr1.start()
            self.threadList.append(thr1)
            thr2 = taskConsoleThread(target, p.stderr, progAndParam[0])
            thr2.start()
            self.threadList.append(thr2)
            #print 'launch ok'
        else:#except:
            print 'launch exception'
        #self.appStarted = True
    def close(self):
        import win32api

        for i in self.pList:
            #print 'processing:', i.pid, int(i._handle)
            processManager.killChildProcessTree(i.pid)
            win32api.TerminateProcess(int(i._handle), -1)
    
        for i in self.threadList:
            i.quit()
