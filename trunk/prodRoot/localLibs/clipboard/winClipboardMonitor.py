import win32gui
import win32api
import win32con
import win32clipboard
'''
CF_BITMAP	A handle to a bitmap (HBITMAP).
CF_DIB	A memory object containing a BITMAPINFO structure followed by the bitmap bits.
CF_DIBV5	Windows 2000/XP: A memory object containing a BITMAPV5HEADER structure followed by the bitmap color space information and the bitmap bits.
CF_DIF	Software Arts' Data Interchange Format.
CF_DSPBITMAP	Bitmap display format associated with a private format. The hMem parameter must be a handle to data that can be displayed in bitmap format in lieu of the privately formatted data.
CF_DSPENHMETAFILE	Enhanced metafile display format associated with a private format. The hMem parameter must be a handle to data that can be displayed in enhanced metafile format in lieu of the privately formatted data.
CF_DSPMETAFILEPICT	Metafile-picture display format associated with a private format. The hMem parameter must be a handle to data that can be displayed in metafile-picture format in lieu of the privately formatted data.
CF_DSPTEXT	Text display format associated with a private format. The hMem parameter must be a handle to data that can be displayed in text format in lieu of the privately formatted data.
CF_ENHMETAFILE	A handle to an enhanced metafile (HENHMETAFILE).
CF_GDIOBJFIRST through CF_GDIOBJLAST	Range of integer values for application-defined Microsoft Windows Graphics Device Interface (GDI) object clipboard formats. Handles associated with clipboard formats in this range are not automatically deleted using the GlobalFree function when the clipboard is emptied. Also, when using values in this range, the hMem parameter is not a handle to a GDI object, but is a handle allocated by the GlobalAlloc function with the GMEM_MOVEABLE flag.
CF_HDROP	A handle to type HDROP that identifies a list of files. An application can retrieve information about the files by passing the handle to the DragQueryFile functions.
CF_LOCALE	The data is a handle to the locale identifier associated with text in the clipboard. When you close the clipboard, if it contains CF_TEXT data but no CF_LOCALE data, the system automatically sets the CF_LOCALE format to the current input language. You can use the CF_LOCALE format to associate a different locale with the clipboard text.

An application that pastes text from the clipboard can retrieve this format to determine which character set was used to generate the text.

Note that the clipboard does not support plain text in multiple character sets. To achieve this, use a formatted text data type such as Rich Text Format (RTF) instead.

Windows NT/2000/XP: The system uses the code page associated with CF_LOCALE to implicitly convert from CF_TEXT to CF_UNICODETEXT. Therefore, the correct code page table is used for the conversion.
CF_METAFILEPICT	Handle to a metafile picture format as defined by the METAFILEPICT structure. When passing a CF_METAFILEPICT handle by means of Dynamic Data Exchange (DDE), the application responsible for deleting hMem should also free the metafile referred to by the CF_METAFILEPICT handle.
CF_OEMTEXT	Text format containing characters in the OEM character set. Each line ends with a carriage return/linefeed (CR-LF) combination. A null character signals the end of the data.
CF_OWNERDISPLAY	Owner-display format. The clipboard owner must display and update the clipboard viewer window, and receive the WM_ASKCBFORMATNAME, WM_HSCROLLCLIPBOARD, WM_PAINTCLIPBOARD, WM_SIZECLIPBOARD, and WM_VSCROLLCLIPBOARD messages. The hMem parameter must be NULL.
CF_PALETTE	Handle to a color palette. Whenever an application places data in the clipboard that depends on or assumes a color palette, it should place the palette on the clipboard as well.
 	If the clipboard contains data in the CF_PALETTE (logical color palette) format, the application should use the SelectPalette and RealizePalette functions to realize (compare) any other data in the clipboard against that logical palette.

When displaying clipboard data, the clipboard always uses as its current palette any object on the clipboard that is in the CF_PALETTE format.
CF_PENDATA	Data for the pen extensions to the Microsoft Windows for Pen Computing.
CF_PRIVATEFIRST through CF_PRIVATELAST	Range of integer values for private clipboard formats. Handles associated with private clipboard formats are not freed automatically; the clipboard owner must free such handles, typically in response to the WM_DESTROYCLIPBOARD message.
CF_RIFF	Represents audio data more complex than can be represented in a CF_WAVE standard wave format.
CF_SYLK	Microsoft Symbolic Link (SYLK) format.
CF_TEXT	Text format. Each line ends with a carriage return/linefeed (CR-LF) combination. A null character signals the end of the data. Use this format for ANSI text.
CF_WAVE	Represents audio data in one of the standard wave formats, such as 11 kHz or 22 kHz Pulse Code Modulation (PCM).
CF_TIFF	Tagged-image file format.
CF_UNICODETEXT	Windows NT/2000/XP: Unicode text format. Each line ends with a carriage return/linefeed (CR-LF) combination. A null character signals the end of the data.
'''
'''
CF_BITMAP
CF_DIB
CF_DIBV5
CF_DIF
CF_DSPBITMAP
CF_DSPENHMETAFILE
CF_DSPMETAFILEPICT
CF_DSPTEXT
CF_ENHMETAFILE
CF_GDIOBJFIRST through CF_GDIOBJLAST
CF_HDROP
CF_LOCALE
CF_METAFILEPICT
CF_OEMTEXT
CF_OWNERDISPLAY
CF_PALETTE
CF_PENDATA
CF_PRIVATEFIRST through CF_PRIVATELAST
CF_RIFF
CF_SYLK
CF_TEXT
CF_WAVE
CF_TIFF
CF_UNICODETEXT
'''

typeDict = {
  win32clipboard.CF_BITMAP:"CF_BITMAP",

  win32clipboard.CF_DIB:"CF_DIB",

  win32clipboard.CF_DIBV5:"CF_DIBV5",

  win32clipboard.CF_DIF:"CF_DIF",

  win32clipboard.CF_DSPBITMAP:"CF_DSPBITMAP",

  win32clipboard.CF_DSPENHMETAFILE:"CF_DSPENHMETAFILE",

  win32clipboard.CF_DSPMETAFILEPICT:"CF_DSPMETAFILEPICT",

  win32clipboard.CF_DSPTEXT:"CF_DSPTEXT",

  win32clipboard.CF_ENHMETAFILE:"CF_ENHMETAFILE",

  #win32clipboard.CF_GDIOBJFIRST through CF_GDIOBJLAST:"CF_GDIOBJFIRST through CF_GDIOBJLAST",

  win32clipboard.CF_HDROP:"CF_HDROP",

  win32clipboard.CF_LOCALE:"CF_LOCALE",

  win32clipboard.CF_METAFILEPICT:"CF_METAFILEPICT",

  win32clipboard.CF_OEMTEXT:"CF_OEMTEXT",

  win32clipboard.CF_OWNERDISPLAY:"CF_OWNERDISPLAY",

  win32clipboard.CF_PALETTE:"CF_PALETTE",

  win32clipboard.CF_PENDATA:"CF_PENDATA",

  #win32clipboard.CF_PRIVATEFIRST through CF_PRIVATELAST:"CF_PRIVATEFIRST through CF_PRIVATELAST",

  win32clipboard.CF_RIFF:"CF_RIFF",

  win32clipboard.CF_SYLK:"CF_SYLK",

  win32clipboard.CF_TEXT:"CF_TEXT",

  win32clipboard.CF_WAVE:"CF_WAVE",

  win32clipboard.CF_TIFF:"CF_TIFF",

  win32clipboard.CF_UNICODETEXT:"CF_UNICODETEXT",
}
import traceback

class clipboardMonitor:
  '''
  referenced http://code.activestate.com/recipes/334779/
  http://code.activestate.com/recipes/355593/
  '''
  def startMonitor(self, gtk_window = None):
    self.setClipBySelf = False
    self.clipboardMonitorEnumClip = True#This is used to indicate if we'll enumerate clipboard
    if gtk_window is None:
      gtk_window = self.window
      #print gtk_window
    self._hwnd = gtk_window.window.handle

    # Sublass the window and inject a WNDPROC to process messages.
    self._oldwndproc = win32gui.SetWindowLong(self._hwnd, win32con.GWL_WNDPROC, self._wndproc)
    
    self.nextWnd = None
    self.captureFlag = False
    try:
      self.nextWnd = win32clipboard.SetClipboardViewer(self._hwnd)
    except win32api.error:
      if win32api.GetLastError () == 0:
        # information that there is no other window in chain
        pass
      else:
        print 'set viewer error'
        raise
    self.nameTypeDict = {}#maintain global clip type?
    
    
  def _wndproc (self, hWnd, msg, wParam, lParam):
    """ A WINDPROC to process window messages. """
    if True:#try:
      if msg == win32con.WM_CHANGECBCHAIN:
        self.OnChangeCBChain (msg, wParam, lParam)
      elif msg == win32con.WM_DRAWCLIPBOARD:
        self.OnDrawClipboard (msg, wParam, lParam)
      # Restore the old WndProc. Notice the use of win32api
      # instead of win32gui here. This is to avoid an error due to
      # not passing a callable object.
      if msg == win32con.WM_DESTROY:
        if self.nextWnd:
          win32clipboard.ChangeClipboardChain (self._hwnd, self.nextWnd)
        else:
          win32clipboard.ChangeClipboardChain (self._hwnd, 0)

        win32api.SetWindowLong (self._hwnd,
                                 win32con.GWL_WNDPROC,
                                 self._oldwndproc)
    else:#except:
      pass
    return win32gui.CallWindowProc(self._oldwndproc, hWnd, msg, wParam,
                                   lParam)
  def OnChangeCBChain (self, msg, wParam, lParam):
    if self.setClipBySelf == False:
        if self.nextWnd == wParam:
          # repair the chain
          self.nextWnd = lParam
        if self.nextWnd:
          # pass the message to the next window in chain
          win32api.SendMessage (self.nextWnd, msg, wParam, lParam)
    else:
        self.setClipBySelf = False
  def clipboardText(self, text):
    print text
  def toggleCapture(self):
    self.captureFlag = not self.captureFlag
  def getClipboardData(self, type):
    if self.nameTypeDict.has_key(type):
      return win32clipboard.GetClipboardData(self.nameTypeDict[type])
    return None
  def setClipboardData(self, type, content):
    win32clipboard.EmptyClipboard()
    self.setClipBySelf = True
    win32clipboard.SetClipboardData(self.nameTypeDict[type], content)

  def OnDrawClipboard (self, msg, wParam, lParam):
    '''
    if self.first:
      self.first = False
    else:
      print "clipboard content changed"
    formats = []
    '''
    self.nameTypeDict = {}
    if self.captureFlag:
      try:
        win32clipboard.OpenClipboard(0)#0 indicates that the clipboard is assosiated with the current task
        #cf = win32clipboard.EnumClipboardFormats(0)
      except:
        print 'open clipboard failed, the clipboard seems not opened'
        return
      try:
        if self.clipboardMonitorEnumClip:
          f = win32clipboard.EnumClipboardFormats(0)
          while f != 0:
            try:
              #print 'clip format:%d,'%f,win32clipboard.GetClipboardFormatName(f)#,':',win32clipboard.GetClipboardData(f)
              self.nameTypeDict[win32clipboard.GetClipboardFormatName(f)] = f
              '''
              if f != 49171:#OLE data will cause error when display
                print '--------------------------------------------------------------------'
                print win32clipboard.GetClipboardData(f)
              '''
            except:
              print 'can not retrieve format:%d'%f
              if typeDict.has_key(f):
                print 'clip format, standard:',typeDict[f]
                self.nameTypeDict[typeDict[f]] = f
              else:
                print 'unknown type,%d'%f
            f = win32clipboard.EnumClipboardFormats(f)
        
        #Call callback
        '''
        try:
            data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            #print 'data:',data
            self.clipboardText(data)
        except:
            print 'get cf text failed'
            traceback.print_exc()
        '''
        try:
          self.clipboardData()
        except TypeError:
            print 'call clipboardData failed'
            traceback.print_exc()
        
        #print self.getClipboardData("CSV")
      except:
          print 'Something wrong processing clipboard data'
          traceback.print_exc()
          pass
      finally:
        #finally will always be execute for the try...finally block
        try:
            win32clipboard.CloseClipboard()
        except:
            print 'close clipboard error'
            traceback.print_exc()

    if self.nextWnd:
      # pass the message to the next window in chain
      win32api.SendMessage (self.nextWnd, msg, wParam, lParam)
