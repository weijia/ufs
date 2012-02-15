
import mimetypes
import posixpath
import sys
import os
import time
import shutil

if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    
def _quote_html(html):
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
class file_request_handler:
  #copy from SimpleHTTPServer.py
  def guess_type(self, path):
      """Guess the type of a file.
  
      Argument is a PATH (a filename).
  
      Return value is a string of the form type/subtype,
      usable for a MIME Content-type header.
  
      The default implementation looks the file's extension
      up in the table self.extensions_map, using application/octet-stream
      as a default; however it would be permissible (if
      slow) to look inside the data to make a better guess.
  
      """
  
      base, ext = posixpath.splitext(path)
      if ext in self.extensions_map:
          return self.extensions_map[ext]
      ext = ext.lower()
      if ext in self.extensions_map:
          return self.extensions_map[ext]
      else:
          return self.extensions_map['']
          
  weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  monthname = [None,
               'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


  if not mimetypes.inited:
      mimetypes.init() # try to read system mime.types
  extensions_map = mimetypes.types_map.copy()
  extensions_map.update({
      '': 'application/octet-stream', # Default
      '.py': 'text/plain',
      '.c': 'text/plain',
      '.h': 'text/plain',
      })

      
  def serveStringFile(self, dataStringFile, path):
        ctype = self.guess_type(path)
        sys.stdout.write("%s %d %s\r\n" %
                 ("HTTP/1.0", 200, 'OK'))
        self.send_header('Server:', "BaseHTTP/0.3")
        self.send_header('Date', self.date_time_string())
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", len(dataStringFile.getvalue()))
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        #print dataStringFile.getvalue()
        self.copyfile(dataStringFile, sys.stdout)
      
  def serve(self, path):
        ctype = self.guess_type(path)
        sys.stdout.write("%s %d %s\r\n" %
                 ("HTTP/1.0", 200, 'OK'))
        self.send_header('Server:', "BaseHTTP/0.3")
        self.send_header('Date', self.date_time_string())
        self.send_header("Content-type", ctype)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            f = open(path, mode)
        except IOError:
            self.send_error(404, "File not found")
            return None
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        if f:
          self.copyfile(f, sys.stdout)
          f.close()
  def copyfile(self, source, outputfile):
      """Copy all data between two file objects.

      The SOURCE argument is a file object open for reading
      (or anything with a read() method) and the DESTINATION
      argument is a file object open for writing (or
      anything with a write() method).

      The only reason for overriding this would be to change
      the block size or perhaps to replace newlines by CRLF
      -- note however that this the default server uses this
      to copy binary data as well.

      """
      shutil.copyfileobj(source, outputfile)        
        
  request_version = 'HTTP/1.0'
  
  
  def send_error(self, code, message=None):
      """Send and log an error reply.

      Arguments are the error code, and a detailed message.
      The detailed message defaults to the short entry matching the
      response code.

      This sends an error response (so it must be called before any
      output has been generated), logs the error, and finally sends
      a piece of HTML explaining the error to the user.

      """

      try:
          short, long = self.responses[code]
      except KeyError:
          short, long = '???', '???'
      if message is None:
          message = short
      explain = long
      #self.log_error("code %d, message %s", code, message)
      # using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
      #content = (self.error_message_format %
      content = ("%(code)\: %(message), %(explain)" %
                 {'code': code, 'message': _quote_html(message), 'explain': explain})
      self.send_response(code, message)
      self.send_header("Content-Type", "text/html")
      self.send_header('Connection', 'close')
      self.end_headers()
      if self.command != 'HEAD' and code >= 200 and code not in (204, 304):
          self.write(content)
  
  def write(self, content):
    sys.stdout.write(content)
    
  def end_headers(self):
      """Send the blank line ending the MIME headers."""
      if self.request_version != 'HTTP/0.9':
          self.write("\r\n")  
  
  def send_header(self, keyword, value):
      """Send a MIME header."""
      if self.request_version != 'HTTP/0.9':
          self.write("%s: %s\r\n" % (keyword, value))

  def date_time_string(self, timestamp=None):
      """Return the current date and time formatted for a message header."""
      if timestamp is None:
          timestamp = time.time()
      year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
      s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
              self.weekdayname[wd],
              day, self.monthname[month], year,
              hh, mm, ss)
      return s
      
  responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

