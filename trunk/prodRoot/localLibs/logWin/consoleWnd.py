#!/usr/bin/env python

# example textview-basic.py
import sys
import os


try:  
    import pygtk  
    pygtk.require ("2.0")  
except:  
    pass  
  
try:  
    import gtk  
    import gtk.glade
except:  
    print "You need to install pyGTK or GTKv2"  
    print "or set your PYTHONPATH correctly."  
    sys.exit(1)  
import os
import gobject
from ConsoleOutputCollector import ConsoleOutputCollector
#import gtkTaskbarIconForConsole

import fileTools

class consoleWnd:
    windowname = 'window1'
    textWndName = 'consoleTextWnd'
    builder = gtk.Builder()
    '''
    This class manages console windows, it will kill applications for every console window.
    '''
        
    def __init__(self, parent):
        gladefile = "consoleWnd.glade"
        fullPath = fileTools.findFileInProduct(gladefile)
        # Loads the UI from GtkBuilder XML file  
        self.builder.add_from_file(fullPath)  
               
        # Lets extract a reference to window object to use later  
        self.window = self.builder.get_object(self.windowname)  

        self.parent = parent
        #self.minimized = False
        window = self.window
        window.set_resizable(True)
        window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        #window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        #window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)

        #window.connect("destroy", self.wnd_close_clicked)
        #window.connect('window-state-event', self.new_window_state)
        window.set_title("Python console log window")
        window.set_border_width(1)
        dic = {
            "destory_cb":self.wnd_close_clicked,
            "minimize_clicked_cb":self.min,
            'topmost_toggled_cb':self.topMost
        }  
        self.builder.connect_signals (dic)  
        self.textview = self.builder.get_object(self.textWndName)
        self.topMostFlag = True
        self.topMost(None)
        
        self.console_output_collector = ConsoleOutputCollector()
        #window.show()
        self.isMinimized = True
        self.window.hide()
    def wnd_close_clicked(self, widget):
        self.close_app()
        
    def close_app(self):
        try:
            #Remove menu item in parent (taskbar menu)
            self.parent.consoleClose(self)
        except:
            pass
        try:
            self.console_output_collector.close()
        except:
            pass
    def updateViewCallback(self, data):
        #print 'callback called'
        #self.data = data
        #print "updateView:", data
        gobject.idle_add(self.updateView, data)
        import time
        time.sleep(0.1)

    def updateView(self, data):
        buf = self.textview.get_buffer()
        buf.insert(buf.get_end_iter(), data)
        #self.data = ''

        
    def topMost(self, widget):
        self.topMostFlag = not self.topMostFlag
        self.window.set_keep_above(self.topMostFlag)

    def min(self, data):
        self.isMinimized = True
        self.window.hide()
        
    def startAppWithParam(self, progAndParam = ['D:\\code\\python\\developing\\ufs\\webserver-cgi.py']):
        cwd = os.path.dirname(progAndParam[0])
        #self.startApp(cwd, progAndParm)
        self.console_output_collector.runConsoleApp(self, cwd, progAndParam)
        self.window.set_title(' '.join(progAndParam))
        self.progAndParam = progAndParam
        
    '''
    def new_window_state(self, widget, event):
        """set the minimized variable to change the title to the same as the statusbar text"""
        if event.changed_mask == gtk.gdk.WINDOW_STATE_ICONIFIED:
            if not self.minimized:
                self.minimized = True
                print 'hide task bar hint'
                self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
            else: # self.minimized:
                self.minimized = False
                print 'create task bar hint'
                self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        return False

    def runApp(self, widget):
        self.quickStart('D:\\sandbox\\developing\\proxySmart\\twistedProxy.py')
    def quickStart(self, appPath):
        p = os.path.dirname(appPath)
        self.startApp(p, [appPath])
    def startApp(self, cwd = 'D:\\code\\python\\developing\\ufs', progAndParm = ['D:\\code\\python\\developing\\ufs\\webserver-cgi.py']):
        #print '------------------------------',progAndParm
        self.console_output_collector.runConsoleApp(self, cwd, progAndParm)
        self.window.set_title(' '.join(progAndParm))
    '''

        
def main():
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    return 0

if __name__ == "__main__":
    consoleWnd(None)
    main()
