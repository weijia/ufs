import pygtk
pygtk.require('2.0')
import gtk
import gtkTaskbarIconForConsole
#import gtkTxtWndMod
import logWnd
import localLibSys
import localLibs.logSys.logDir as logDir
import gtkDropTarget
import gtkDragMove
import fileTools
from advScriptRunnerV3 import advScriptRunner
from TagDialog import TagDialog
import urllib

class AdvScriptRunnerWithTag(advScriptRunner):
    '''
    def __init__(self):
        super(AdvScriptRunnerWithTag, self).__init__()
        '''
    def startApplicationsNoReturn(self, l, launchServiceThreadClass):
        '''
        from dbus.mainloop.glib import threads_init
        threads_init()
        '''
        self.initialApps = l
        self.dialog = TagDialog()
        self.startScriptRunnerApp(launchServiceThreadClass)
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        print 'after gtk.gdk.threads_leave()'
        self.quitAll()
        print 'final quit'
        import sys
        sys.exit()
        return 0
    def dropped(self, wid, context, x, y, data, info, time):
        # Got data.
        #print data.data
        #print data.format
        #print data.selection
        #print data.target
        #print data
        #print data.data
        #print data.get_targets()
        #Dropped file has a prefix of "file:///", remove it.
        '''
        pa = data.data.replace('file:///','')
        #print '------------------------------dropped:', pa
        pa = pa.replace('\r','').replace('\n','').replace(chr(0),'')
        import re
        if (re.search("\.bat$", pa) is None) and (re.search("\.py$", pa) is None) and (re.search("\.exe$", pa) is None):
            #Normal file
            print pa
        else:
            self.startAppWithParam([pa])
        '''
        pa = data.data.split("\n")
        res = []
        for i in pa:
            v = i.replace('\r','').replace('\n','').replace(chr(0),'')
            if v == "":
                continue
            res.append(urllib.unquote(v))
        self.dialog.set_data(res)
        self.dialog.show_dialog()
        
        context.finish(True, False, time)
        
    def on_info(self, widget):
        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, "Download completed")
        md.run()
        md.destroy()
        