#Boa:Frame:consoleManager

import wx
from fileDropTarget import *
import consoleWin
import os
import urllib

def create(parent):
    return consoleManager(parent)

initialStartApp = ['D:\\tagfs\\webserver-cgi.py',
'D:\\sandbox\\ufs\\webroot\\webserver-cgi.py',
'D:\\tagfs\\app\\sysDirectoryHandler.py']

taskAppListPath = 'D:\\tagfs\\bgTasks.txt'

#
# Create the custom event.
#
appStartEVT_CUSTOM_EVENT_type = wx.NewEventType()
appStartEVT_CUSTOM_EVENT = wx.PyEventBinder(appStartEVT_CUSTOM_EVENT_type, 1)

class appStartEvent(wx.PyEvent):
    def __init__(self, event_type, id, appParams):
        wx.PyEvent.__init__(self, id, event_type)
        # Note that the id and event_type are reversed
        # from wx.PyCommandEvent
        self.appParams = appParams


class appStarterConsole(consoleWin.consoleWin):
    appStartString = 'startBackgroundApp?'
    def __init__(self, parent, manager):
        consoleWin.consoleWin.__init__(self, parent, True)
        self.manager = manager
    def outputLine(self, line):
        consoleWin.consoleWin.outputLine(self, line)
        pos = line.find(self.appStartString)
        if pos != -1:
            rest = line[pos+len(self.appStartString):]
            print 'rest:',rest
            end = rest.find(' HTTP')
            app = rest[:end]
            print 'app',app
            param = urllib.unquote(app)
            print 'param',param
            appParam = param.split(' ')
            if True:
                evt = appStartEvent(appStartEVT_CUSTOM_EVENT_type, self.manager.GetId(), appParam)
                #self.manager.GetEventHandler().ProcessEvent(evt)
                wx.PostEvent(self.manager.GetEventHandler(), evt)
    def onClose(self):
        consoleWin.consoleWin.onClose(self)
        self.manager.onClientClose(self)

[wxID_CONSOLEMANAGER] = [wx.NewId() for _init_ctrls in range(1)]

from taskbarIconManager import *

class consoleManager(taskbarIconManager):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_CONSOLEMANAGER, name=u'consoleManager',
              parent=prnt, pos=wx.Point(569, 302), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title=u'consoleManager')
        self.SetClientSize(wx.Size(392, 223))

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.showTaskBarIcon()
        dt3 = FileDropTarget(self)
        # Link the Drop Target Object to the Text Control
        self.SetDropTarget(dt3)
        #self.consoleWnds = []
        self.consoleApp = {}
        self.Bind(appStartEVT_CUSTOM_EVENT, self.onAppStartEvent, id=self.GetId())
        try:
            f = open(taskAppListPath, 'r')
            initApp = f.readlines()
        except:
            initApp = initialStartApp
        for i in initApp:
            i = i.replace('\n','')
            i = i.replace('\r','')
            if i[0] != '#':
              self.addFile(i)
    def onAppStartEvent(self, event):
        self.addFile(event.appParams[0], event.appParams[1:])
        
    def addFile(self, filename, param = []):
        #print filename
        #self.fileList.AppendItems([filename])
        newWin = appStarterConsole(None, self)
        newMenuId = wx.NewId()
        self.consoleApp[newMenuId] = [os.path.basename(filename), newMenuId, newWin]
        #self.consoleWnds.append(newWin)
        self.bindTaskbarMenu(self.onTaskbarMenuRightClick, newMenuId)
        args = [filename]
        args.extend(param)
        newWin.runConsoleApp(os.path.dirname(filename), args)
        newWin.Show(True)
        #newWin.SetFocus()
        print 'started app'
        
    def onTaskbarMenuRightClick(self, event):
        #wx.MessageBox('Hello From TaskBarIcon!', 'Prompt')
        self.consoleApp[event.GetId()][2].Show()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for i in self.consoleApp.keys():
            menu.Append(i, self.consoleApp[i][0])
        return menu
    def closeCallback(self, event):
        #Called when closing the main frame
        for i in self.consoleApp.keys():
            try:
                self.consoleApp[i][2].Close()
            except wx._core.PyDeadObjectError:
                pass
    def onClientClose(self, client):
        for i in self.consoleApp.keys():
            if self.consoleApp[i][2] == client:
                del self.consoleApp[i]
