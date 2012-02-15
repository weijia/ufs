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
col1 = gtk.TreeViewColumn("Foo", cell, active = 0)
col2 = gtk.TreeViewColumn("host", cell2, text = 1)
tv.append_column(col1)
tv.append_column(col2)

w = gtk.Window()
w.connect("destroy", gtk.main_quit)
w.show()

w.add(tv)
tv.show()

## Some initial data
model.append([True, "good"])
model.append([False, "bad"])

gtk.main()