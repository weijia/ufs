#!/usr/bin/env python

# example dirWin.py

import pygtk
pygtk.require('2.0')
import gtk

class Base:
    def __init__(self):
        #self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #handler1 = self.window.connect("destroy",self.destroy)
        #self.window.show()
        self.dia = gtk.FileChooserDialog(title=None, parent=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=None, backend=None)
        self.dia.run()
        #gtk.main_quit()
        
    def destroy(self,widget,data=None):
        gtk.main_quit()
            
    def main(self):
        gtk.main()

    
print __name__
if __name__ == "__main__":
    base = Base()
    #base.main()