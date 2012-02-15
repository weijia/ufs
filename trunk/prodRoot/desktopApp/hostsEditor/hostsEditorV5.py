import gtk
import gobject
import re

        

class hostsEditorWin(gtk.Window):
    def __init__(self, *args):
        gtk.Window.__init__(self, *args)
        self.filePath = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        self.connect("destroy", gtk.main_quit)

        model = gtk.ListStore(bool, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.model = model
        cell = gtk.CellRendererToggle()
        cell.connect("toggled", self.on_toggle, model)
        cell2 = gtk.CellRendererText()

        cell2.set_property('editable', True)
        ####################################
        #Here active=0 means the active attribute for CellRendererToggle is located in list store index 0
        col1 = gtk.TreeViewColumn("Enabled", cell, active = 0)
        col2 = gtk.TreeViewColumn("ip address", cell2, text = 1)
        col3 = gtk.TreeViewColumn("hostname", cell2, text = 2)
        col4 = gtk.TreeViewColumn("comment", cell2, text = 3)
        
        tv = gtk.TreeView(model)
        tv.connect("button_press_event", self.dbClick)
        
        tv.append_column(col1)
        tv.append_column(col2)
        tv.append_column(col3)
        tv.append_column(col4)

        self.set_size_request(500,500)


        menu_bar = gtk.MenuBar()

        file_item = gtk.MenuItem("File")
        file_item.show()
        file_menu = gtk.Menu()    # Don't need to show menus

        # Create the menu items
        open_item = gtk.MenuItem("Load")
        save_item = gtk.MenuItem("Save")
        quit_item = gtk.MenuItem("Quit")
        new_item = gtk.MenuItem("New")

        # Add them to the menu
        file_menu.append(new_item)
        file_menu.append(open_item)
        file_menu.append(save_item)
        file_menu.append(quit_item)

        # Attach the callback functions to the activate signal
        open_item.connect_object("activate", self.menuitem_response, "file.open")
        save_item.connect_object("activate", self.menuitem_response, "file.save")
        new_item.connect_object("activate", self.menuitem_response, "file.new")

        # We can attach the Quit menu item to our exit function
        quit_item.connect_object ("activate", gtk.main_quit, "file.quit")

        # We do need to show menu items
        open_item.show()
        save_item.show()
        quit_item.show()
        new_item.show()

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)
        vbox = gtk.VBox(False, 2)
        
        self.filePathEntry = gtk.Entry()
        self.filePathEntry.set_text(self.filePath)
        self.add(vbox)
        file_menu.show()
        self.filePathEntry.show()
        vbox.pack_start(menu_bar, False, False, 2)
        vbox.pack_start(self.filePathEntry, False, False, 2)
        vbox.pack_start(scrolled_window)
        vbox.show()
        menu_bar.show()

        tv.show()
        self.loadFromFile(self.filePath)
        scrolled_window.add_with_viewport(tv)
        scrolled_window.show()
        self.show()
    def menuitem_response(self, event):
        #print event
        if event == "file.new":
            self.model.append([False, "ip address", "hostname","#comments"])
        elif event == "file.open":
            self.loadFromFile(self.filePathEntry.get_text())
    def destroy(self, event):
        print event
    def on_toggle(self, cell, path, model, *ignore):
        if path is not None:
            it = self.model.get_iter(path)
            self.model[it][0] = not self.model[it][0]
            
    def on_dbclick(self, cell, path, model, *ignore):
        print cell, path, model, ignore
        
    def loadFromFile(self, filePath):
        self.model.clear()
        ## Some initial data
        cnt = 0
        f = open(filePath, "r")
        for i in f.readlines():
            m = re.search('^\#*\s*((\d+\.)+\d+)\s+(([\w\-]+\.)+[\w\-]+)\s*(\#.*)*$', i)
            if m is None:
                print i
                continue
            #Remove leading spaces
            while i[0] == ' ':
                i=i[1:]
            # print 'group0:',m.group(0),'group1:', m.group(1),'group2:', m.group(2),'group3:', m.group(3),'group4:', m.group(4), 'group5:', m.group(5),#'group6:', m.group(6),
            # print  '    ===================='
            # print ''
            if i[0] == "#":
                self.model.append([False, m.group(1), m.group(3), m.group(5)])
            else:
                self.model.append([True, m.group(1), m.group(3), m.group(5)])

            cnt += 1
        

    def dbClick(self, widget, event):
        print widget, event
        if event.type == gtk.gdk._2BUTTON_PRESS:
            self.model.append([False, "ip address", "hostname","#comments"])

if __name__=="__main__":
    w = hostsEditorWin()
    gtk.main()