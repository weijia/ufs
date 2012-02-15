import wx
from MyTaskBarIcon import *

class taskbarIconManager(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_CONSOLEMANAGER, name=u'consoleManager',
              parent=prnt, pos=wx.Point(569, 302), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title=u'consoleManager')
        self.SetClientSize(wx.Size(392, 223))
        
    def showTaskBarIcon(self):
        self.taskBarIcon = MyTaskBarIcon(self, 'Console manager')
        self.Bind(wx.EVT_ICONIZE, self.OnTaskbarIconManagerIconize)
        self.Bind(wx.EVT_CLOSE, self.OnTaskbarIconManagerClose)
    
    def isShowIconOnly(self):
        return True
    
    def OnTaskbarIconManagerIconize(self, event):
        if self.isShowIconOnly():
            self.Show(False)
        event.Skip()

    def OnTaskbarIconManagerClose(self, event):
        #try:
        if True:
            self.closeCallback(event)
        print 'Destroying taskbar icon'
        self.taskBarIcon.Destroy()

            
        event.Skip()
        
    def closeCallback(self, event):
        pass
    def bindTaskbarMenu(self, callback, menuId):
        self.taskBarIcon.Bind(wx.EVT_MENU, callback, id=menuId)
