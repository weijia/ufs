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
    '''
    This class will generate the floating element and the task bar icon.
    '''
    def dropped(self, wid, context, x, y, data, info, time):
        # Got data.
        #print data.data
        #print data.format
        #print data.selection
        #print data.target
        #print data
        #print data.data
        #print data.get_targets()
        #Dropped file has a prefix of "file:///", remove it. And quoted using urllib.quote so " " is now %20
        pa = data.data.replace('file:///','')
        #print '------------------------------dropped:', pa
        pa = pa.replace('\r','').replace('\n','').replace(chr(0),'')
        self.create_console_wnd_for_app([pa])
        context.finish(True, False, time)

    def drop_cb(self, wid, context, x, y, time):#Without this callback, got_data_cb will not be called
        # Some data was dropped, get the data
        wid.drag_get_data(context, context.targets[-1], time)
        return True
    def clickM(self, mTxt):
        self.app_name_to_task_dict[mTxt].show()
    def consoleClose(self, t):
        '''
        Remove the coresponding menu item for the task
        '''
        self.icon.rmMenuItem(self.task_to_menu_item_dict[t])
        for i in self.app_name_to_task_dict.keys():
            if self.app_name_to_task_dict[i] == t:
                del self.app_name_to_task_dict[i]
                break
      
    def startScriptRunnerApp(self):
        self.task_to_menu_item_dict = {}
        self.app_name_to_task_dict = {}
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
            if fullP is None:
                fullP = fileTools.findAppInProduct(i)
                if fullP is None:
                    print i, 'not found'
            #print '-----------------------------',fullP
            self.create_console_wnd_for_app([fullP])
        #w.set_skip_taskbar_hint(True)#Hide taskbar icon

    def close_application(self, widget):
        #self.window.hide()
        print 'killing applications'
        for i in self.task_to_menu_item_dict.keys():
            i.close_application(widget)
        self.icon.set_visible(False)
        gtk.main_quit()
        print 'all application killed, after main_quit'
      

    def create_console_wnd_for_app(self, param):
        '''
        Start an app with full path and parameters passed in a list
        param: [appFullPath, param1, param2, ...]
        '''
        l = logDir.logDir(str(param))
        t = logWnd.logWnd(self, l.getLogFilePath())
        t.startAppWithParam(param)
        cnt = 1
        app_path_and_param_gen_str = str(param)
        if self.app_name_to_task_dict.has_key(app_path_and_param_gen_str):
            while self.app_name_to_task_dict.has_key(app_path_and_param_gen_str + '-' + str(cnt)):
                cnt +=1
            app_path_and_param_gen_str = app_path_and_param_gen_str + '-' + str(cnt)
          
        self.app_name_to_task_dict[app_path_and_param_gen_str] = t
        self.task_to_menu_item_dict[t] = self.icon.addMenuItem(app_path_and_param_gen_str)
        
        
              
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
