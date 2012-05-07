#!/usr/bin/env python 

import pygtk
import gtk
pygtk.require("2.0") 
#import colormap
import fileTools
#import libSys
#import localLibSys
import wwjufsdatabase.libs.tag.tagSystemInterfaceV2 as tagSystem
import wwjufsdatabase.libs.utils.transform as transform


class TagDialog(object):
    def __init__(self):
        
        self.builder = gtk.Builder()
        gladefile = "TagDialog.glade"
        fullPath = fileTools.findFileInProduct(gladefile)
        # Loads the UI from GtkBuilder XML file  
        self.builder.add_from_file(fullPath)  
               
        # Lets extract a reference to window object to use later  
        #self.window = self.builder.get_object(self.windowname)  

        #self.minimized = False
        #window = self.window
        #window.set_resizable(True)
        #window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        
        
        #self.builder.add_from_file("tagDialog.glade")
        self.window1 = self.builder.get_object("dialog1")
        #self.liststore1 = self.builder.get_object("liststore1")
        #self.liststore1.append(["good"])
        self.list = self.builder.get_object("treeview1")
        self.liststore = gtk.ListStore(int, str)
        self.liststore.append([False,'red'])
        self.liststore.append([True,'green'])
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
        #self.window1.show()
        dic = {
            "on_ok_button_clicked":self.on_ok_button_clicked,
            "on_cancel_button_clicked": self.on_cancel_button_clicked,
        }  
        self.builder.connect_signals(dic)
        
    def set_data(self, item_list):
        self.liststore.clear()
        for i in item_list:
            self.liststore.append([True, i])
            
    def show_dialog(self):
        self.window1.show()
        
    def on_cell_toggled(self, widget, path):
        self.liststore[path][0] = not self.liststore[path][0]
        
    def on_cancel_button_clicked(self, widget, data = None):
        self.window1.hide()
        
    def on_ok_button_clicked(self, widget, data=None):
        import wwjufsdatabase.libs.services.servicesV2 as service
        req = service.req()
        #gtk.main_quit()
        entry = self.builder.get_object("entry1")
        tag = entry.get_text()
        print tag
        tag_list_raw = tag.split(",")
        tag_list = []
        for i in tag_list_raw:
            if i == "":
                continue
            tag_list.append(unicode(i))
        t = tagSystem.getTagSysObj(req.getDbSys())
        for i in self.liststore:
            #print i[0], i[1]
            if i[0]:
                url = i[1]
                url = url.replace("file:///", "")
                full_path = transform.transformDirToInternal(url)
                #print "full_path is:", full_path
                t.tag(full_path, tag_list)
        self.window1.hide()


if __name__ == "__main__":
    app = TagDialog()
    gtk.main()