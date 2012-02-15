class dropTarget:
  def got_data_cb(self, wid, context, x, y, data, info, time):
      # Got data.
      #print data.data
      #print data.format
      #print data.selection
      #print data.target
      self.callback(wid, context, x, y, data, info, time)
      context.finish(True, False, time)

  def drop_cb(self, wid, context, x, y, time):#Without this callback, got_data_cb will not be called
      # Some data was dropped, get the data
      wid.drag_get_data(context, context.targets[-1], time)
      return True
      
  def setDropTarget(self, gtkWin = None, callback = None):
      if gtkWin is None:
        self.dropTargetWnd = self.window
      else:
        self.dropTargetWnd = gtkWin
      self.dropTargetWnd.drag_dest_set(0, [], 0)
      self.dropTargetWnd.connect('drag_drop', self.drop_cb)
      self.dropTargetWnd.connect('drag_data_received', self.got_data_cb)
      if callback is None:
        self.callback = self.dropped
      else:
        self.callback = callback
  def dropped(self, wid, context, x, y, data, info, time):
      pass