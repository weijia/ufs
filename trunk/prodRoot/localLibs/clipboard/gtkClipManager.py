#!/usr/bin/env python  
  
import sys 
import traceback

try:  
  import pygtk  
  pygtk.require ("2.0")  
except:  
  pass  
  
if True:#try:  
  import gtk  
  import gtk.glade  
#except:
else:
  print "You need to install pyGTK or GTKv2"  
  print "or set your PYTHONPATH correctly."  
  sys.exit(1)  

  
clipTypeNames = ['CF_TEXT', 'CSV']
  
  
import winClipboardMonitor

class gtkClipManagerWnd(winClipboardMonitor.clipboardMonitor):  
  builder = gtk.Builder()
  oroginalTextWndName = 'clipboardText'
  windowname = "clipManagerMainWnd"#This name should be the exact window name in the glade file. 
  scriptWndName = "scriptText"
  targetTextWndName = 'targetText'
  clipTypeComboName = 'clipTypeCombo'
  scriptTree = 'scriptTree'
  def __init__(self):  
      gladefile = "gtkClipManager.glade"  
      import uuid
      self.filename = 'script/'+str(uuid.uuid4())+'.py'
      # Loads the UI from GtkBuilder XML file  
      self.builder.add_from_file(gladefile)  
             
      # Lets extract a reference to window object to use later  
      self.window = self.builder.get_object(self.windowname)  
      #print self.window
      self.startMonitor()
      # Sets up event handlers  
      
      dic = {  
          #"on_btnFetch_clicked" : self.fetchTweet,
          "menuNewClick":self.scriptText,
          "menuOpenClick":self.executeScriptCode,
          "on_MainWindow_destroy" : gtk.main_quit,
          "fileOpenMenu": self.openFile,
          "toggle_toggled_cb": self.stopCapture,
          "saveFile_activate_cb":self.saveFile,
          "saveAs_activate_cb":self.saveAsFile,
          "topmost_toggled_cb":self.topMost,
          "autoTransform_toggled_cb":self.autoTransform
      }  
      self.builder.connect_signals (dic)  
      #self.pg1_clipboard.wait_for_text()
      #topMost will toggle flag and set top most
      self.topMostFlag = False
      #self.topMost(None)
      self.combo = self.builder.get_object(self.clipTypeComboName)
      import gobject
      store = gtk.ListStore(gobject.TYPE_STRING)
      for i in clipTypeNames:
        store.append ([i])
      self.combo.set_model(store)
      self.combo.set_text_column(0)
      self.combo.set_active(0)
      #self.scriptText(None)
      
      self.scriptTreeWnd = self.builder.get_object(self.scriptTree)
      #Create the listStore Model to use with the wineView
      self.pathList = gtk.ListStore(str, str, str, str)
      column = gtk.TreeViewColumn('Script Path', gtk.CellRendererText(), text=0)
      column.set_resizable(True)
      #column.set_sort_column_id(columnId)
      self.scriptTreeWnd.append_column(column)
      #Attatch the model to the treeView
      self.scriptTreeWnd.set_model(self.pathList)
      self.autoTransformFlag = False
      return
  def autoTransform(self, widget):
    self.autoTransformFlag = not self.autoTransformFlag
    print 'autoTransformFlag:',self.autoTransformFlag
  def topMost(self, widget):
    self.topMostFlag = not self.topMostFlag
    self.window.set_keep_above(self.topMostFlag)
  def stopCapture(self, widget):
    self.toggleCapture()
  def clipboardText(self, data):
    return
    #original = self.builder.get_object(self.oroginalTextWndName)
    #original.get_buffer().set_text(data)
  def clipboardData(self):
    print 'clipboard data called----------------------'
    type = self.combo.child.get_text()
    print 'current type is:',type
    data = self.getClipboardData(type)
    #print 'data is:',data
    if data is None:
      return
    original = self.builder.get_object(self.oroginalTextWndName)
    data = data.replace('\x00', '').decode('utf-8', 'replace').encode('utf-8')
    original.get_buffer().set_text(data)
    try:
      self.executeScriptCode(None)
    except:
      print 'Something wrong when executing codes'
      traceback.print_exc()
      pass
  def scriptText(self, widget):
    sw = self.builder.get_object(self.scriptWndName)
    data = '''#x = x.replace('\\r','')
#xl = x.split('\\n')

#if y is None:
#  y = '\\n'.join(yl)
#target.get_buffer().set_text(y)
    '''
    sw.get_buffer().set_text(data)
  def openFile(self, widget):
    chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
    response = chooser.run()
    if response == gtk.RESPONSE_OK:
      filename = chooser.get_filename()
      print filename, 'selected'
      f = open(filename, 'r')
      self.filename = filename
      sw = self.builder.get_object(self.scriptWndName)
      data = f.read()
      sw.get_buffer().set_text(data)
    elif response == gtk.RESPONSE_CANCEL:
        print 'Closed, no files selected'
    chooser.destroy()
    
  def saveFile(self, widget):
    sc = self.getText(self.scriptWndName)
    f = open(self.filename,'w')
    f.write(sc)
    f.close()
    
  def saveAsFile(self, widget):
    print 'save as'
    chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))

    response = chooser.run()
    if response == gtk.RESPONSE_OK:
      filename = chooser.get_filename()
      print filename, 'selected'
      f = open(filename, 'w')
      self.filename = filename
      self.saveFile(widget)
    elif response == gtk.RESPONSE_CANCEL:
        print 'Closed, no files selected'
    chooser.destroy()
    
    
  def getText(self, widgetName):
    sw = self.builder.get_object(widgetName)
    return sw.get_buffer().get_text(sw.get_buffer().get_start_iter(),sw.get_buffer().get_end_iter())
    
  def executeScriptCode(self, widget):
    sc = self.getText(self.scriptWndName)
    #print 'script is:',sc
    x = self.getText(self.oroginalTextWndName)
    x = x.replace('\r','')
    xl = x.split('\n')
    y = None
    t = None
    exec sc
    #print y
    target = self.builder.get_object(self.targetTextWndName)
    if y is None:
      y = '\n'.join(yl)
      #print y
    target.get_buffer().set_text(y)
    if self.autoTransformFlag:
      if (t is None) or t:
        print 'setting text to %s'%y
        type = self.combo.child.get_text()
        print 'current type is:',type
        self.setClipboardData(type,y)
    
      
      

def main():
  myapp = gtkClipManagerWnd()  
  gtk.main()
  
if __name__ == '__main__':
  main()
