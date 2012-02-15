#!/usr/bin/env python

# example dirSelection.py

import pygtk
pygtk.require('2.0')
import gtk
from optparse import OptionParser
import dbus

BUS_NAME_NAME = 'com.wwjufsdatabase.logService'
INTERFACE_NAME = 'com.wwjufsdatabase.logService'
OBJECT_NAME = '/service'

def getDir(busName, interface, obj):
    dia = gtk.FileChooserDialog(title=None, parent=None, action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=("OK", 
            gtk.RESPONSE_OK), backend=None)
    #print dia.run()#-5
    #print int(gtk.RESPONSE_OK)#-5
    if dia.run() == int(gtk.RESPONSE_OK):
        bus = dbus.SessionBus()
        proxy = bus.get_object(busName, obj)
        #print proxy.notify(dia.get_filenames(), dbus_interface = interface)
        print proxy.logStr(dia.get_filenames()[0], dbus_interface = interface)


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-b", "--bus", action="store",help="interface name for notifying", default = BUS_NAME_NAME)
    parser.add_option("-i", "--interface", action="store",help="interface name for notifying", default = INTERFACE_NAME)
    parser.add_option("-o", "--object", action="store", help="object for notifying", default = OBJECT_NAME)
    (options, args) = parser.parse_args()

    getDir(options.bus, options.interface, options.object)
