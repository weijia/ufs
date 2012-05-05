import consoleWnd
import localLibSys
from localLibs.logSys.logSys import *
import gobject
import beanstalkc
from localLibs.services.beanstalkdServices.BeanstalkdLauncherService import BeanstalkdLauncherService

MAX_DISPLAYED_LINE_NUM = 400
REMOVE_LINE_NUMBER = 300
MAX_DISPLAY_TEXT_NUM = 40000

class logWnd(consoleWnd.consoleWnd):
    def __init__(self, parent, logFilePath = None):
        consoleWnd.consoleWnd.__init__(self, parent)
        #self.lastLine = ''
        #self.curLines = []
        self.kept_text = ''
        self.stopped = False
        if logFilePath is None:
            self.logFile = None
        else:
            self.logFile = open(logFilePath, 'w')
    
    def close_app(self):
        cl("killing app:", self.progAndParam)
        consoleWnd.consoleWnd.close_app(self)
        if self.logFile is None:
            return
        self.logFile.close()
        self.logFile = None
        
    def wnd_close_clicked(self, widget):
        self.send_stop_signal()
        
    def send_stop_signal(self):
        if not self.stopped:
            try:
                b = BeanstalkdLauncherService()
                for i in self.console_output_collector.pList:
                    b.addItem({"cmd":"stop", "pid": i.pid})
                    cl("sending stop cmd to: ", i.pid)
            except beanstalkc.SocketError:
                pass
            self.timer_id = gobject.timeout_add(5000, self.close_app)#Here time value are milliseconds
            self.stopped = True

            
    def updateView(self, data):
        #print "updateView:", data
        if not (self.logFile is None):
            self.logFile.write(data)
        if not self.isMinimized:
            self.realUpdateView(data)
        else:
            '''
            #Save the data so logs can be displayed when the console window is not minimized
            self.lastLine += data
            if self.lastLine == '':
                #No logs yet
                return
            newLines = self.lastLine.splitlines()

            if self.lastLine[-1] in ['\r\n']:
                #End with \r \n, add new lines to line buffer: curLines. and set new lastLine
                self.lastLine = ''
                self.curLines.extend(newLines)
            else:
                self.curLines.extend(newLines[0:-1])
                self.lastLine = newLines[-1]

            #cl(self.curLines)
            line_count = len(self.curLines)
            if line_count >= MAX_DISPLAYED_LINE_NUM:
                #Remove some lines
                line_number = line_count - REMOVE_LINE_NUMBER
                self.curLines = self.curLines[line_number:]
                #cl('removed lines')
            '''
            self.kept_text += data
            if len(self.kept_text) > MAX_DISPLAY_TEXT_NUM:
                previous_line_n = self.kept_text.rfind("\n", MAX_DISPLAY_TEXT_NUM)
                previous_line_r = self.kept_text.rfind("\r", MAX_DISPLAY_TEXT_NUM)
                previous_line_end = max([previous_line_n, previous_line_r])
                self.kept_text = self.kept_text[previous_line_end+1:]
                    
            
    def realUpdateView(self, data):
        buf = self.textview.get_buffer()
        line_count = buf.get_line_count()
        if line_count >= MAX_DISPLAYED_LINE_NUM:
            #Remove some lines
            line_number = line_count - REMOVE_LINE_NUMBER
            iter = buf.get_iter_at_line(line_number)
            startIter = buf.get_iter_at_offset(0)
            buf.delete(startIter, iter)
        buf.insert(buf.get_end_iter(), data)
        
    def show(self, *args):
        cl('show called')
        if not self.isMinimized:
            return
        '''
        buf = self.textview.get_buffer()
        ncl('setting text', self.curLines)
        buf.set_text(('\r\n').join(self.curLines)+self.lastLine)
        self.curLines = []
        self.lastLine = ''
        '''
        buf = self.textview.get_buffer()
        buf.set_text("")
        buf.insert(buf.get_end_iter(), self.kept_text)
        self.kept_text = ''
        self.isMinimized = False
        self.window.show(*args)
        
    def min(self, data):
        ncl('min called')
        buf = self.textview.get_buffer()
        self.kept_text = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        consoleWnd.consoleWnd.min(self, data)
        #False means do not get hidden text
        #self.curLines = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False).splitlines()