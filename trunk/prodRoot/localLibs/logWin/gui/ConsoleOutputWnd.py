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
#from ConsoleOutputCollector import ConsoleOutputCollector
#import gtkTaskbarIconForConsole
from localLibs.logSys.logSys import *

import fileTools
MAX_DISPLAY_TEXT_NUM = 40000
MAX_DISPLAYED_LINE_NUM = 400
REMOVE_LINE_NUMBER = 300

class ConsoleOutputWnd:
    windowname = 'window1'
    textWndName = 'consoleTextWnd'
    builder = gtk.Builder()
    '''
    This class manages console windows, it will kill applications for every console window.
    '''
        
    def __init__(self, parent, logFilePath = None):
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

        #window.connect("destroy", self.on_quit_clicked)
        #window.connect('window-state-event', self.new_window_state)
        window.set_title("Python console log window")
        window.set_border_width(1)
        dic = {
            "destory_cb":self.on_close_clicked,
            "minimize_clicked_cb":self.min,
            'topmost_toggled_cb':self.topMost
        }  
        self.builder.connect_signals (dic)  
        self.textview = self.builder.get_object(self.textWndName)
        self.topMostFlag = True
        self.topMost(None)
        
        #self.console_output_collector = ConsoleOutputCollector()
        #window.show()
        self.isMinimized = True
        self.window.hide()
        self.kept_text = ''
        self.stopped = False
        if logFilePath is None:
            self.logFile = None
        else:
            self.logFile = open(logFilePath, 'w')
            
            
    def on_close_clicked(self, widget):
        self.parent.console_wnd_close_clicked(self)
        
    def updateViewCallback(self, data):
        #print 'callback called'
        #self.data = data
        #print "updateView:", data
        gobject.idle_add(self.updateView, data)
        import time
        time.sleep(0.1)


    def updateView(self, data):
        #print "updateView:", data
        if not (self.logFile is None):
            self.logFile.write(data)
        if not self.isMinimized:
            self.realUpdateView(data)
        else:
            self.kept_text += data
            if len(self.kept_text) > MAX_DISPLAY_TEXT_NUM:
                previous_line_n = self.kept_text.rfind("\n", MAX_DISPLAY_TEXT_NUM)
                previous_line_r = self.kept_text.rfind("\r", MAX_DISPLAY_TEXT_NUM)
                previous_line_end = max([previous_line_n, previous_line_r])
                self.kept_text = self.kept_text[previous_line_end+1:]
                    
            
    def realUpdateView(self, data):
        buf = self.textview.get_buffer()
        line_count = buf.get_line_count()
        if line_count >= MAX_DISPLAYED_LINE_NUM:
            #Remove some lines
            line_number = line_count - REMOVE_LINE_NUMBER
            iter = buf.get_iter_at_line(line_number)
            startIter = buf.get_iter_at_offset(0)
            buf.delete(startIter, iter)
        buf.insert(buf.get_end_iter(), data)
        
    def show(self, *args):
        cl('show called')
        if not self.isMinimized:
            return
        buf = self.textview.get_buffer()
        buf.set_text("")
        buf.insert(buf.get_end_iter(), self.kept_text)
        self.kept_text = ''
        self.isMinimized = False
        self.window.show(*args)
        
    def min(self, data):
        ncl('min called')
        buf = self.textview.get_buffer()
        #False means do not get hidden text
        self.kept_text = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        self.isMinimized = True
        self.window.hide()
        
    def topMost(self, widget):
        self.topMostFlag = not self.topMostFlag
        self.window.set_keep_above(self.topMostFlag)
        

