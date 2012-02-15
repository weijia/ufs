#!/usr/bin/env python

# example dirSelection.py

import pygtk
pygtk.require('2.0')
import gtk


if __name__ == "__main__":
    dia = gtk.FileChooserDialog(title=None, parent=None, action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=("OK", 
            gtk.RESPONSE_OK), backend=None)
    #print dia.run()#-5
    #print int(gtk.RESPONSE_OK)#-5
    if dia.run() == int(gtk.RESPONSE_OK):
        print dia.get_filenames()
