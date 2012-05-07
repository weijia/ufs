import pygtk
pygtk.require('2.0')
import gtk
#import gtkTxtWndMod
#import logWnd
import localLibSys
import localLibs.logSys.logDir as logDir
from localLibs.logWin.gui.TagDialog import TagDialog
import urllib

class TagDropHandler:
    def __init__(self):
        self.dialog = TagDialog()
    def on_dropped(self, wid, context, x, y, data, info, time):
        pa = data.data.split("\n")
        res = []
        for i in pa:
            v = i.replace('\r','').replace('\n','').replace(chr(0),'')
            if v == "":
                continue
            res.append(urllib.unquote(v))
        self.dialog.set_data(res)
        self.dialog.show_dialog()
        
    def on_info(self, widget):
        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, "Download completed")
        md.run()
        md.destroy()
        