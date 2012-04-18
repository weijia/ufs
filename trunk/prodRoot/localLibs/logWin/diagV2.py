#!/usr/bin/env python 

import pygtk
import gtk
pygtk.require("2.0") 

class GUI(object):
  def __init__(self):
      builder = gtk.Builder()
      builder.add_from_file("tagDialog.glade")
      builder.connect_signals(self)
      self.window1 = builder.get_object("dialog1")
      self.window1.show()

  def on_window1_destroy(self,widget,data=None):
      gtk.main_quit()

  def on_button1_clicked(self,widget,data=None):
      gtk.main_quit()  

if __name__ == "__main__":
  app = GUI()
  gtk.main()