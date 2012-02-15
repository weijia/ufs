



class directoryTreeWnd:
  def fillDirectory(self, treeWnd = None):
    if treeWnd is None:
      self.treeWnd = self.window
    else:
      self.treeWnd = treeWnd

    #self.treeWnd = self.builder.get_object(self.scriptTree)
    #Create the listStore Model to use with the wineView
    self.pathList = gtk.ListStore(str, str, str, str)
    column = gtk.TreeViewColumn('Script Path', gtk.CellRendererText(), text=0)
    column.set_resizable(True)
    #column.set_sort_column_id(columnId)
    self.treeWnd.append_column(column)
    #Attatch the model to the treeView
    self.treeWnd.set_model(self.pathList)
    
    
  def AddColumn(self, title, columnId):
    '''This function adds a column to the list view.
    First it create the gtk.TreeViewColumn and then set
    some needed properties
    '''

    column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
    column.set_resizable(True)
    column.set_sort_column_id(columnId)
    self.treeWnd.append_column(column)
    
    
  def OnAddItem(self, item):
    '''Called when the use wants to add a wine'''
    #Create the dialog, show it, and store the results
    self.pathList.append(item)