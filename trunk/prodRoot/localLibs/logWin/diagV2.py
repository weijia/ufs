#!/usr/bin/env python 

import pygtk
import gtk
pygtk.require("2.0") 
#import colormap

class GUI(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("tagDialog.glade")
        self.window1 = self.builder.get_object("dialog1")
        #self.liststore1 = self.builder.get_object("liststore1")
        #self.liststore1.append(["good"])
        self.list = self.builder.get_object("treeview1")
        self.liststore = gtk.ListStore(int, str)
        self.liststore.append([0,'red'])
        self.liststore.append([1,'green'])
        #iter = liststore.insert(1, (2,'blue',colormap.alloc_color('blue')) )
        #iter = liststore.insert_after(iter, [3,'yellow',colormap.alloc_color('blue')])
        
        ###################################
        # Add checkbox
        ###################################
        # From http://stackoverflow.com/questions/5707495/problem-with-checkboxes-in-a-pygtk-treeview
        # And ref: http://python-gtk-3-tutorial.readthedocs.org/en/latest/cellrenderers.html
        cell = gtk.CellRendererToggle()
        #cell.connect("toggled", on_toggle, model)
        col = gtk.TreeViewColumn("select", cell, active=0)
        cell.connect("toggled", self.on_cell_toggled)
        
        ###################################
        # Add title of column
        ###################################
        #column = gtk.TreeViewColumn("index")
        column_file_path = gtk.TreeViewColumn("file_path")
        #self.list.append_column(column)
        self.list.append_column(col)
        self.list.append_column(column_file_path)
        
        ###################################
        # Display list store data
        ###################################
        # From http://learngtk.org/pygtk-tutorial/liststore.html
        '''
        cell = gtk.CellRendererText()
        col.pack_start(cell, False)
        col.add_attribute(cell, "text", 0)
        '''
        cell_file_path = gtk.CellRendererText()
        column_file_path.pack_start(cell_file_path, False)
        column_file_path.add_attribute(cell_file_path, "text", 1)
        
        self.list.set_model(self.liststore)
        self.window1.show()
        dic = {
            "on_ok_button_clicked":self.on_window1_destroy,
        }  
        self.builder.connect_signals(dic)
        
    def on_cell_toggled(self, widget, path):
            self.liststore[path][0] = not self.liststore[path][0]
         
    def on_window1_destroy(self,widget,data=None):
        print"good"
        gtk.main_quit()

    def on_button1_clicked(self,widget,data=None):
        gtk.main_quit()  

if __name__ == "__main__":
    app = GUI()
    gtk.main()