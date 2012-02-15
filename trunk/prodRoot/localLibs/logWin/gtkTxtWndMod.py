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
from wndConsole import *
gtk.gdk.threads_init()
import gtkTaskbarIconForConsole

import fileTools

class consoleWnd:
    windowname = 'window1'
    textWndName = 'consoleTextWnd'
    builder = gtk.Builder()

    def close_application(self, widget):
        try:
          self.parent.consoleClose(self)
        except:
          pass
        try:
          self.wC.close()
        except:
          pass
    def updateViewCallback(self, data):
        #print 'callback called'
        self.data = data
        gobject.idle_add(self.updateView, None)
        import time
        time.sleep(0.1)

    def updateView(self, param):
        buf = self.textview.get_buffer()
        buf.insert(buf.get_end_iter(), self.data)
        self.data = ''
        
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
        '''
        Gdk::WINDOW_TYPE_HINT_NORMAL, 
        Gdk::WINDOW_TYPE_HINT_DIALOG, 
        Gdk::WINDOW_TYPE_HINT_MENU, 
        Gdk::WINDOW_TYPE_HINT_TOOLBAR, 
        Gdk::WINDOW_TYPE_HINT_SPLASHSCREEN, 
        Gdk::WINDOW_TYPE_HINT_UTILITY, 
        Gdk::WINDOW_TYPE_HINT_DOCK, 
        Gdk::WINDOW_TYPE_HINT_DESKTOP, 
        Gdk::WINDOW_TYPE_HINT_DROPDOWN_MENU, 
        Gdk::WINDOW_TYPE_HINT_POPUP_MENU, 
        Gdk::WINDOW_TYPE_HINT_TOOLTIP, 
        Gdk::WINDOW_TYPE_HINT_NOTIFICATION, 
        Gdk::WINDOW_TYPE_HINT_COMBO, 
        '''
        #window.connect("destroy", self.close_application)
        #window.connect('window-state-event', self.new_window_state)
        window.set_title("Python console log window")
        window.set_border_width(1)
        dic = {
            "destory_cb":self.close_application,
            "minimize_clicked_cb":self.min,
            'topmost_toggled_cb':self.topMost
        }  
        self.builder.connect_signals (dic)  
        self.textview = self.builder.get_object(self.textWndName)
        self.topMostFlag = True
        self.topMost(None)
        
        '''
        box1 = gtk.VBox(False, 0)
        window.add(box1)
        box1.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(2)
        box1.pack_start(box2, True, True, 0)
        box2.show()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        self.textview = textview
        textbuffer = textview.get_buffer()
        sw.add(textview)
        sw.show()
        textview.show()
        box2.pack_start(sw)
        
        #self.icon = gtkTaskbarIconForConsole.MyStatusIcon(self)
        
        button2 = gtk.Button("minimize")
        button2.connect("clicked", self.min)
        box2.pack_start(button2, False, True, 0)
        button2.set_flags(gtk.CAN_DEFAULT)
        button2.grab_default()
        button2.show()
        '''
        self.wC = wndConsole()
        #window.show()
        self.isMinimized = True
        self.window.hide()
        
    def topMost(self, widget):
        self.topMostFlag = not self.topMostFlag
        self.window.set_keep_above(self.topMostFlag)

    def min(self, data):
        self.isMinimized = True
        self.window.hide()
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
    '''
    def runApp(self, widget):
        self.quickStart('D:\\sandbox\\developing\\proxySmart\\twistedProxy.py')
    def quickStart(self, appPath):
        p = os.path.dirname(appPath)
        self.startApp(p, [appPath])
    def startApp(self, cwd = 'D:\\code\\python\\developing\\ufs', progAndParm = ['D:\\code\\python\\developing\\ufs\\webserver-cgi.py']):
        #print '------------------------------',progAndParm
        self.wC.runConsoleApp(self, cwd, progAndParm)
    def startAppWithParam(self, progAndParm = ['D:\\code\\python\\developing\\ufs\\webserver-cgi.py']):
        cwd = os.path.dirname(progAndParm[0])
        self.startApp(cwd, progAndParm)
        
def main():
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    return 0

if __name__ == "__main__":
    consoleWnd(None)
    main()
