import gtk
import gobject
import re

def on_toggle(cell, path, model, *ignore):
    if path is not None:
        it = model.get_iter(path)
        model[it][0] = not model[it][0]
def on_dbclick(cell, path, model, *ignore):
    print cell, path, model, ignore
    
        
    
model = gtk.ListStore(bool, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
tv = gtk.TreeView(model)

def dbClick(widget, event):
    print widget, event
    if event.type == gtk.gdk._2BUTTON_PRESS:
        model.append([False, "ip address", "hostname","#comments"])
        
tv.connect("button_press_event", dbClick)

cell = gtk.CellRendererToggle()
cell.connect("toggled", on_toggle, model)
cell2 = gtk.CellRendererText()
#cell2.connect("dblclick", on_dbclick, model)
cell2.set_property('editable', True)
####################################
#Here active=0 means the active attribute for CellRendererToggle is located in list store index 0
col1 = gtk.TreeViewColumn("Enabled", cell, active = 0)
col2 = gtk.TreeViewColumn("ip address", cell2, text = 1)
col3 = gtk.TreeViewColumn("hostname", cell2, text = 2)
col4 = gtk.TreeViewColumn("comment", cell2, text = 3)
tv.append_column(col1)
tv.append_column(col2)
tv.append_column(col3)
tv.append_column(col4)

w = gtk.Window()
w.connect("destroy", gtk.main_quit)
w.set_size_request(500,500)

def menuitem_response(event):
    #print event
    if event == "file.new":
        model.append([False, "ip address", "hostname","#comments"])
def destroy(event):
    print event
    
menu_bar = gtk.MenuBar()

file_item = gtk.MenuItem("File")
file_item.show()
file_menu = gtk.Menu()    # Don't need to show menus

# Create the menu items
open_item = gtk.MenuItem("Open")
save_item = gtk.MenuItem("Save")
quit_item = gtk.MenuItem("Quit")
new_item = gtk.MenuItem("New")

# Add them to the menu
file_menu.append(new_item)
file_menu.append(open_item)
file_menu.append(save_item)
file_menu.append(quit_item)

# Attach the callback functions to the activate signal
open_item.connect_object("activate", menuitem_response, "file.open")
save_item.connect_object("activate", menuitem_response, "file.save")
new_item.connect_object("activate", menuitem_response, "file.new")

# We can attach the Quit menu item to our exit function
quit_item.connect_object ("activate", destroy, "file.quit")

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
vbox.pack_start(menu_bar, False, False, 2)
vbox.pack_start(scrolled_window)
w.add(vbox)
file_menu.show()

'''
w.add(menu_bar)
w.add(scrolled_window)
'''
vbox.show()
menu_bar.show()

## Some initial data
cnt = 0
f = open("C:\\Windows\\System32\\drivers\\etc\\hosts", "r")
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
        model.append([False, m.group(1), m.group(3), m.group(5)])
    else:
        model.append([True, m.group(1), m.group(3), m.group(5)])

    cnt += 1
tv.show()

scrolled_window.add_with_viewport(tv)
scrolled_window.show()
w.show()

gtk.main()