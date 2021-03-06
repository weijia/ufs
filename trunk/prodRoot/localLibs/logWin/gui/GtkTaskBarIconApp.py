import pygtk
pygtk.require('2.0')
import gtk
import gtkTaskbarIconForConsole
from DragDropAndMoveBehavior import DragDropAndMoveBehavior
#import gtkTxtWndMod
#import logWnd
#import localLibSys
#import localLibs.logSys.logDir as logDir
#import gtkDropTarget
#import gtkDragMove
#import fileTools
#import beanstalkc
#from localLibs.services.beanstalkdServices.beanstalkServiceBaseV2 import gBeanstalkdServerHost, gBeanstalkdServerPort

class GtkTaskBarIconApp(object):
    '''
    This class will generate the floating element and the task bar icon.
    '''
    def __init__(self, parent = None):
        if parent is None:
            self.parent = self
        else:
            self.parent = parent
        w = gtk.Window()
        self.window = w
        w.set_size_request(100, 100)
        w.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)#Hide from the taskbar.
        self.icon = gtkTaskbarIconForConsole.MyStatusIcon(self.parent)
        w.set_keep_above(True)
        w.set_opacity(0.5)
        w.set_decorated(False)#Disable window frame board
        self.drag_drop_behavior = DragDropAndMoveBehavior(self.parent)
        self.drag_drop_behavior.startDragMove(w)
        self.drag_drop_behavior.setDropTarget(w, self.on_dropped)
        
        #The following must be behind the above operations,
        #otherwise, drag drop function will fail
        #the following errors are printed if the order is wrong
        #E:\codes\git\ufs.git\trunk\prodRoot\localLibs\logWin\gui\gtkDragMove.py:18: GtkW
        #arning: gtk_widget_set_events: assertion `!GTK_WIDGET_REALIZED (widget)' failed
        #  | gtk.gdk.BUTTON_RELEASE_MASK)#set_events must be called before connect
        
        w.connect('destroy', lambda w: gtk.main_quit())
        w.connect('window-state-event', self.window_state_event_cb)
        w.show_all()
    def window_state_event_cb(self, window, event):
        if event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED:
            if event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED:
                print 'Window was minimized!'
            else:
                print 'Window was unminimized!'
        return True
    def start_gui_msg_loop(self):
        #The threads_init method must be called, otherwise, gtk will not run in multi thread mode, in such case
        #the output of the console window will not be output until gtk receive other events from UI (the console
        #app will continue only when the floating wnd were dragged etc.
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        return 0
    
    #######################################
    # The following handler is just examples
    #######################################
    def on_quit_clicked(self):
        gtk.main_quit()
        
    def on_dropped(self, wid, context, x, y, data, info, time):
        print data.data
        
    def on_menu_clicked(self, menu_text):
        pass
        
    def console_wnd_close_clicked(self):
        pass
    
def main():
    g = GtkTaskBarIconApp()
    g.start_gui_msg_loop()

if __name__ == "__main__":
    main()
