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

class dropRunWnd(gtkDropTarget.dropTarget, gtkDragMove.dragMove):
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
        pa = data.data.replace('file:///','')
        #print '------------------------------dropped:', pa
        pa = pa.replace('\r','').replace('\n','').replace(chr(0),'')
        self.startAppWithParam([pa])
        context.finish(True, False, time)

    def drop_cb(self, wid, context, x, y, time):#Without this callback, got_data_cb will not be called
        # Some data was dropped, get the data
        wid.drag_get_data(context, context.targets[-1], time)
        return True
    def clickM(self, mTxt):
        self.mD[mTxt].show()
    def consoleClose(self, t):
        self.icon.rmMenuItem(self.tL[t])
        for i in self.mD.keys():
            if self.mD[i] == t:
                del self.mD[i]
                break
      
    def startScriptRunnerApp(self):
        self.tL = {}
        self.mD = {}
        w = gtk.Window()
        self.window = w
        w.set_size_request(100, 100)
        w.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)#Hide from the taskbar.
        w.connect('destroy', lambda w: gtk.main_quit())
        self.startDragMove()
        self.setDropTarget()
        self.icon = gtkTaskbarIconForConsole.MyStatusIcon(self)
        w.set_keep_above(True)
        w.set_opacity(0.5)
        w.set_decorated(False)#Disable window frame board, work in company machine
        w.show_all()
        for i in self.initialApps:
            fullP = fileTools.findFileInProduct(i)
            #print '-----------------------------',fullP
            self.startAppWithParam([fullP])
        #w.set_skip_taskbar_hint(True)#Hide taskbar icon

    def close_application(self, widget):
        #self.window.hide()
        # try:
            # print 'calling close_application'
            # from dbus.mainloop.glib import threads_init
            # threads_init()
            # print 'after threads_init'
            # import appStarterForDbusQuitApp
            # print 'calling stopService'
            # appStarterForDbusQuitApp.stopService()
        # except:
            # pass
        print 'killing applications'
        for i in self.tL.keys():
            i.close_application(widget)
        self.icon.set_visible(False)
        gtk.main_quit()
        print 'all application killed, after main_quit'
      

    def startAppWithParam(self, param):
        '''
        Start an app with full path and parameters passed in a list
        param: [appFullPath, param1, param2, ...]
        '''
        l = logDir.logDir(str(param))
        t = logWnd.logWnd(self, l.getLogFilePath())
        t.startAppWithParam(param)
        cnt = 1
        paN = str(param)
        if self.mD.has_key(paN):
            while self.mD.has_key(paN + '-' + str(cnt)):
                cnt +=1
            paN = paN + '-' + str(cnt)
          
        self.mD[paN] = t
        self.tL[t] = self.icon.addMenuItem(paN)
        
#    def startApp(self, pa):
#        '''
#        pa is the fullPath for the application that are executing. And there is no param for it. So if it is an short cut, create param from shortcut
#        '''
#        param = [pa]
#        self.startAppWithParam(param)
        
              
def startApplicationsNoReturn(l):
    d = dropRunWnd()
    d.initialApps = l
    d.startScriptRunnerApp()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    return 0
    
  
def main():
    startApplicationsNoReturn([])

if __name__ == "__main__":
    main()
