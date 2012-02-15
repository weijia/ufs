import gtk


def on_toggle(cell, path, model, *ignore):
    if path is not None:
        it = model.get_iter(path)
        model[it][0] = not model[it][0]

model = gtk.ListStore(bool)
tv = gtk.TreeView(model)

cell = gtk.CellRendererToggle()
cell.connect("toggled", on_toggle, model)
col = gtk.TreeViewColumn("Foo", cell, active=0)
tv.append_column(col)

w = gtk.Window()
w.connect("destroy", gtk.main_quit)
w.show()

w.add(tv)
tv.show()

## Some initial data
model.append([True])
model.append([False])

gtk.main()