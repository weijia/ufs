import gtk
import gobject
import re

def on_toggle(cell, path, model, *ignore):
    if path is not None:
        it = model.get_iter(path)
        model[it][0] = not model[it][0]

model = gtk.ListStore(bool, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
tv = gtk.TreeView(model)

cell = gtk.CellRendererToggle()
cell.connect("toggled", on_toggle, model)
cell2 = gtk.CellRendererText()

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

scrolled_window = gtk.ScrolledWindow()
scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

w.add(scrolled_window)


## Some initial data
cnt = 0
f = open("D:\\Windows\\System32\\drivers\\etc\\hosts", "r")
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