import gtk
import gobject


def on_toggle(cell, path, model, *ignore):
    if path is not None:
        it = model.get_iter(path)
        model[it][0] = not model[it][0]

model = gtk.ListStore(bool, gobject.TYPE_STRING)
tv = gtk.TreeView(model)

cell = gtk.CellRendererToggle()
cell.connect("toggled", on_toggle, model)
cell2 = gtk.CellRendererText()

####################################
#Here active=0 means the active attribute for CellRendererToggle is located in list store index 0
col1 = gtk.TreeViewColumn("Enabled", cell, active = 0)
col2 = gtk.TreeViewColumn("host", cell2, text = 1)
tv.append_column(col1)
tv.append_column(col2)

w = gtk.Window()
w.connect("destroy", gtk.main_quit)
w.set_size_request(500,500)

scrolled_window = gtk.ScrolledWindow()
scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

w.add(scrolled_window)


## Some initial data
cnt = 0
f = open("C:\\Windows\\System32\\drivers\\etc\\hosts", "r")
for i in f.readlines():
    #Remove leading spaces
    while i[0] == ' ':
        i=i[1:]
    if i[0] == "#":
        model.append([False, i])
    else:
        model.append([True, i])

    cnt += 1
tv.show()

scrolled_window.add_with_viewport(tv)
scrolled_window.show()
w.show()

gtk.main()