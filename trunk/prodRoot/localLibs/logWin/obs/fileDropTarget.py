import wx
#Get from http://wiki.wxpython.org/DragAndDrop?highlight=%28drop%29|%28drag%29
# Define File Drop Target class
class FileDropTarget(wx.FileDropTarget):
   """ This object implements Drop Target functionality for Files """
   def __init__(self, obj):
      """ Initialize the Drop Target, passing in the Object Reference to
          indicate what should receive the dropped files """
      # Initialize the wsFileDropTarget Object
      wx.FileDropTarget.__init__(self)
      # Store the Object Reference for dropped files
      self.obj = obj

   def OnDropFiles(self, x, y, filenames):
      """ Implement File Drop """
      # For Demo purposes, this function appends a list of the files dropped at the end of the widget's text
      # Move Insertion Point to the end of the widget's text
      '''
      self.obj.SetInsertionPointEnd()
      # append a list of the file names dropped
      self.obj.WriteText("%d file(s) dropped at %d, %d:\n" % (len(filenames), x, y))
      for file in filenames:
         self.obj.WriteText(file + '\n')
      self.obj.WriteText('\n')
      '''
      #print filenames
      for file in filenames:
        #print file
        self.obj.addFile(file)