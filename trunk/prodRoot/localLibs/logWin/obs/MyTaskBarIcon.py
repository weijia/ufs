import wx

##
# The TaskBarIcon class
#
class MyTaskBarIcon(wx.TaskBarIcon):
    ID_Hello = wx.NewId()
    ##
    # \brief the constructor
    #
    def __init__(self, frame, prompt = 'hello world'):
        wx.TaskBarIcon.__init__(self)
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIconBar(prompt)
        #The following codes is added for click event
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        #self.Bind(wx.EVT_MENU, self.OnHello, id=self.ID_Hello)
    def SetIconBar(self, prompt = 'hello world'):
        image = wx.EmptyImage(16,16)

        bmp = image.ConvertToBitmap()
        bmp.SetMask(wx.Mask(bmp, wx.WHITE)) #sets the transparency colour to white 

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(bmp)
        self.SetIcon(icon, prompt)
    #The following methods are added for handling events
    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
            self.frame.Raise()


    def OnHello(self, event):
        wx.MessageBox('Hello From TaskBarIcon!', 'Prompt')
        
    # override
    def CreatePopupMenu(self):
        '''
        menu = wx.Menu()
        menu.Append(self.ID_Hello, 'Hello')
        return menu
        '''
        return self.frame.CreatePopupMenu()
