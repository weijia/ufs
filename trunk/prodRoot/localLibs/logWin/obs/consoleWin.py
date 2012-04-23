#Boa:Frame:consoleWin

import wx
import wx.richtext
import sys
import wx.stc
import Queue

def create(parent):
    return consoleWin(parent)

[wxID_CONSOLEWIN, wxID_CONSOLEWINRICHTEXTCTRL1, wxID_CONSOLEWINTOOLBAR1, 
] = [wx.NewId() for _init_ctrls in range(3)]

#
# Create the custom event.
#
myEVT_CUSTOM_EVENT = wx.NewEventType()
EVT_CUSTOM_EVENT = wx.PyEventBinder(myEVT_CUSTOM_EVENT, 1)

class MyEvent(wx.PyEvent):
    def __init__(self, event_type, id, lines):
        wx.PyEvent.__init__(self, id, event_type)
        # Note that the id and event_type are reversed
        # from wx.PyCommandEvent
        self.lines = lines

import os
import subprocess
import threading
import select
import socket
from MyTaskBarIcon import *

class readThread(threading.Thread):
    def __init__(self, frame, fileD):
        self.frame = frame
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.fileD = fileD
    def run ( self ):
        import uuid
        print 'running'
        #l = open(str(uuid.uuid4()),'w')
        while not self.quitFlag:
            err = self.fileD.readline()
            if err == '':
                print 'err is empty'
                self.quit()
            if err is None:
                self.quit()
                print 'quit'
                break
            '''
            try:
                evt = MyEvent(myEVT_CUSTOM_EVENT, self.frame.GetId(), err)
                self.frame.GetEventHandler().ProcessEvent(evt)
            except:
                print 'send event error'
            '''
            #l.write(err)
            self.frame.q.put(err)
        print 'quit'
        #l.close()
    def quit(self):
        self.quitFlag = True

class TestThread(threading.Thread):
    def __init__(self, frame, fileD):
        self.reader = readThread(self, fileD)
        self.frame = frame

        self.q = Queue.Queue()
        self.quitFlag = False
        threading.Thread.__init__(self)
    def run(self):
        self.reader.start()
        #l = open(str(uuid.uuid4()),'w')
        while not self.quitFlag:
            try:
                err = ''
                err += self.q.get(True, 10)#Wait for 10 seconds
                #print err
                self.q.task_done()
                while not self.q.empty():
                    line = self.q.get()
                    err += line
                    #print line
                    self.q.task_done()
                try:
                    evt = MyEvent(myEVT_CUSTOM_EVENT, self.frame.GetId(), err)
                    #print err
                    self.frame.GetEventHandler().ProcessEvent(evt)
                except:
                    print 'send event error'
            except Queue.Empty:
                #print 'empty'
                pass
        #l.close()
    def quit(self):
        self.quitFlag = True
        self.reader.quit()

[wxID_CONSOLEWINSHOWICONONLYITEMS0] = [wx.NewId() for _init_coll_showIconOnly_Items in range(1)]

class consoleWin(wx.Frame):
    def _init_coll_fileMenu_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.showIconOnly, title=u'View')

    def _init_coll_showIconOnly_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_CONSOLEWINSHOWICONONLYITEMS0,
              kind=wx.ITEM_CHECK, text=u'showIconOnly')

    def _init_utils(self):
        # generated method, don't edit
        self.fileMenu = wx.MenuBar()

        self.showIconOnly = wx.Menu(title=u'')

        self._init_coll_fileMenu_Menus(self.fileMenu)
        self._init_coll_showIconOnly_Items(self.showIconOnly)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_CONSOLEWIN, name=u'consoleWin',
              parent=prnt, pos=wx.Point(470, 217), size=wx.Size(400, 257),
              style=wx.DEFAULT_FRAME_STYLE, title=u'console')
        self._init_utils()
        self.SetClientSize(wx.Size(392, 223))
        self.SetToolTipString(u'console')
        self.SetMenuBar(self.fileMenu)
        self.Bind(wx.EVT_CLOSE, self.OnConsoleWinClose)
        self.Bind(wx.EVT_ICONIZE, self.OnConsoleWinIconize)

        self.toolBar1 = wx.ToolBar(id=wxID_CONSOLEWINTOOLBAR1, name='toolBar1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(392, 28),
              style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        self.SetToolBar(self.toolBar1)

        self.richTextCtrl1 = wx.richtext.RichTextCtrl(id=wxID_CONSOLEWINRICHTEXTCTRL1,
              parent=self, pos=wx.Point(0, 28), size=wx.Size(392, 175),
              style=wx.richtext.RE_MULTILINE, value=u'richTextCtrl1')
        self.richTextCtrl1.SetAutoLayout(True)
        self.richTextCtrl1.Center(wx.BOTH)
        self.richTextCtrl1.SetLabel(u'')
        self.richTextCtrl1.Enable(True)
        self.richTextCtrl1.SetEditable(False)

    def __init__(self, parent, registeredTaskBarIcon = False):
        self._init_ctrls(parent)
        #self.appStarted = False
        self.Bind(EVT_CUSTOM_EVENT, self.OnMyEvent, id=self.GetId())
        self.log_collector_thread_list = []
        try:
            self.runConsoleApp(os.path.dirname(sys.argv[1]), sys.argv[1:])#Param 2 is the app
        except IndexError:
            print 'please assign an app to start'
        self.registeredTaskBarIcon = registeredTaskBarIcon
        if not self.registeredTaskBarIcon:
            self.taskBarIcon = MyTaskBarIcon(self, sys.argv[1])
        self.showIconOnly.FindItemById(wxID_CONSOLEWINSHOWICONONLYITEMS0).Check()
        import uuid
        from time import gmtime, strftime, localtime
        self.logF = open('logs/'+strftime("%Y%m%d_%H_%M_%S", localtime())+str(uuid.uuid4())+'.log', 'w')


    def runConsoleApp(self, cwd, progAndParm):
        self.cwd = cwd
        self.progAndParm = progAndParm
        #self.prog = ['D:\\cygwin\\bin\\ls.exe','-l']
        self.prog = ['c:/python25/pythonw.exe','-u']
        self.prog.extend(progAndParm)#Param 2 is the app
        #self.prog.append('D:\\code\\python\\webserver-cgi.py')
        #self.cwd = 'D:\\code\\python\\'
        #self.cwd = sys.argv[1]#Param 1 is the cwd
        '''
        import os
        self.cwd = os.getcwd()
        '''
        print self.prog
        self.SetTitle(progAndParm[0])
        try:
            self.p = subprocess.Popen(self.prog, cwd = self.cwd, stdout = subprocess.PIPE, stderr = subprocess.PIPE,bufsize=0)
            thr1 = TestThread(self, self.p.stdout)
            thr1.start()
            self.log_collector_thread_list.append(thr1)
            thr2 = TestThread(self, self.p.stderr)
            thr2.start()
            self.log_collector_thread_list.append(thr2)
        except:
          pass
        #self.appStarted = True

    def OnMyEvent(self, event):
        #print event
        #print event.lines
        self.outputLine(event.lines)
        #print 'OnMyEvent'
        #self.outputLine('OnMyEvent\r\n')
        event.Skip()

    def outputLine(self, lines):
        '''
        self.logText.DocumentEnd()
        self.logText.AddText(line)
        if self.logText.GetLineCount() > 800:
            self.logText.SetCurrentPos(0)
            #self.logText.SetSelectionEnd(self.logText.GetLineEndPosition(300))
            self.logText.SelectAll()
            self.logText.ReplaceSelection('')
            self.logText.DocumentEnd()
        '''
        self.outputLineUsingRichText(lines)
    def outputLineUsingRichText(self, lines):
        o = ''.join(lines)
        #print o
        self.logF.write(o)
        self.richTextCtrl1.Freeze()
        self.richTextCtrl1.AppendText(o)
        if self.richTextCtrl1.GetNumberOfLines()> 800:
            self.richTextCtrl1.Clear()
        self.richTextCtrl1.Thaw()
    def OnConsoleWinClose(self, event):
        self.onClose()
        event.Skip()
    def onClose(self):
        try:
            for i in self.log_collector_thread_list:
                i.quit()
            if len(self.log_collector_thread_list):
                self.killSelf()
            #import time
            #time.sleep(5)
        except:
            print 'error'
        try:
            if not self.registeredTaskBarIcon:
                print 'destorying icon'
                self.taskBarIcon.Destroy()
        except:
            print 'error 2'

        
    def killSelf(self):
        import win32api
        win32api.TerminateProcess(int(self.p._handle), -1)

    def OnConsoleWinIconize(self, event):
        if self.showIconOnly.FindItemById(wxID_CONSOLEWINSHOWICONONLYITEMS0).IsChecked():
            self.Show(False)
        event.Skip()
