import gtk

class dragMove:
  def __init__(self):
      self.mouseDown = False

      
  def startDragMove(self, gtkWin = None):
      if gtkWin is None:
        self.dragMoveWnd = self.window
      else:
        self.dragMoveWnd = gtkWin

      self.dragMoveWnd.set_events(gtk.gdk.EXPOSURE_MASK
        | gtk.gdk.LEAVE_NOTIFY_MASK
        | gtk.gdk.BUTTON_PRESS_MASK
        | gtk.gdk.POINTER_MOTION_MASK
        | gtk.gdk.BUTTON_RELEASE_MASK)#set_events must be called before connect

      self.dragMoveWnd.connect("button_press_event", self.button_press_event)
      self.dragMoveWnd.connect("motion_notify_event", self.motion_notify_event)
      self.dragMoveWnd.connect("button_release_event", self.button_release_event)

      self.screen = gtk.gdk.screen_get_default()
      
  def button_press_event(self, widget, event):
    if event.button == 1:
      self.x, self.y = self.dragMoveWnd.get_position()
      #print self.x,',',self.y
      self.mousex, self.mousey = event.x_root, event.y_root
      #print self.mousex,',',self.mousey
      self.mouseDown = True
      
  def motion_notify_event(self, widget, event):
      if self.mouseDown:
        #print 'motion'
        #Drag window
        #print event.x,',',event.y
        #print event.x_root,',',event.y_root
        self.dragMoveWnd.move(int(self.x + event.x_root - self.mousex), int(self.y + event.y_root - self.mousey))
  def button_release_event(self, widget, event):
      #print 'release'
      self.mouseDown = False
