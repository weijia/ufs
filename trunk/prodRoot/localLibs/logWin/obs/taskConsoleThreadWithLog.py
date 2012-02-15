'''
Created on 2011-9-22

@author: Richard
'''
import threading

class taskConsoleThreadWithLog(threading.Thread):
    def __init__(self, target, fileD, logFilePath, appname = 'unknown'):
        self.target = target
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.fileD = fileD
        self.appname = appname
        self.logFilePath
    def run(self):
        #print 'running'
        f = open(self.logFilePath, 'w')
        while not self.quitFlag:
            #print 'before readline'
            err = self.fileD.readline()
            #print 'after readline'
            if err == '':
                #print 'err is empty'
                f.close()
                self.quit()
            if err is None:
                f.close()
                self.quit()
                #print 'quit'
                break
            #print 'got output:',err
            self.target.updateViewCallback(err)
        print 'quitting run: ',self.appname
    def quit(self):
        self.quitFlag = True
