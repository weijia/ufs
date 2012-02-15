import gtkTxtWndMod as consoleWnd
#import localLibSys
from localLibs.logSys.logSys import *

MAX_DISPLAYED_LINE_NUM = 400
REMOVE_LINE_NUMBER = 300


class logWnd(consoleWnd.consoleWnd):
    def __init__(self, parent, logFilePath = None):
        consoleWnd.consoleWnd.__init__(self, parent)
        self.lastLine = ''
        self.curLines = []
        if logFilePath is None:
            self.logFile = None
        else:
            self.logFile = open(logFilePath, 'w')
        
    def updateView(self, param):
        if not (self.logFile is None):
            self.logFile.write(self.data)
        if not self.isMinimized:
            self.realUpdateView(self.data)
        else:
            self.lastLine += self.data
            newLines = self.lastLine.splitlines()
            if self.lastLine == '':
                return
            if self.lastLine[-1] in ['\r\n']:
                self.curLines.extend(newLines[0:-1])
                self.lastLine = newLines[-1]
            else:
                self.lastLine = ''
                self.curLines.extend(newLines)
            #cl(self.curLines)
            line_count = len(self.curLines)
            if line_count >= MAX_DISPLAYED_LINE_NUM:
                #Remove some lines
                line_number = line_count - REMOVE_LINE_NUMBER
                self.curLines = self.curLines[line_number:]
                #cl('removed lines')
            
    def realUpdateView(self, param):
        buf = self.textview.get_buffer()
        line_count = buf.get_line_count()
        if line_count >= MAX_DISPLAYED_LINE_NUM:
            #Remove some lines
            line_number = line_count - REMOVE_LINE_NUMBER
            iter = buf.get_iter_at_line(line_number)
            startIter = buf.get_iter_at_offset(0)
            buf.delete(startIter, iter)
        buf.insert(buf.get_end_iter(), self.data)
        
    def show(self, *args):
        cl('show called')
        if not self.isMinimized:
            return
        buf = self.textview.get_buffer()
        ncl('setting text', self.curLines)
        buf.set_text(('\n').join(self.curLines)+self.lastLine)
        self.curLines = []
        self.lastLine = ''
        self.isMinimized = False
        self.window.show(*args)
        
    def min(self, data):
        cl('min called')
        consoleWnd.consoleWnd.min(self, data)
        buf = self.textview.get_buffer()
        #False means do not get hidden text
        self.curLines = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False).splitlines()