import gtk
import gtk.glade

def main():
    #dialog_glade = gtk.glade.XML("tagDialog.glade", "main_dialog")
    builder = gtk.Builder()
    gladefile = "tagDialog.glade"
    # Loads the UI from GtkBuilder XML file  
    builder.add_from_file(gladefile)  
    dialog = builder.get_widget("dialog1")
    #running the dialog.
    dialog.output = dialog.run()
    #return value of the above command is the response id of the button pressed.
    if dialog.output == 1:
        print "Button 1 pressed"