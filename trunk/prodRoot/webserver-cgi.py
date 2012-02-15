#!/usr/bin/env python
import localLibs.webServer.webServerCgi as webServerCgi
import BaseHTTPServer
from SocketServer import ThreadingMixIn
import sys

'''
import urlparse
import posixpath
import urllib
import os
'''
# Import Psyco if available
'''
try:
    import psyco
    psyco.full()
except ImportError:
    print 'error'
    pass
# ...your code here...
    

'''
class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""

class MyRequestHandler(webServerCgi.CGIHTTPRequestHandler):
    # In diesem Verzeichnis sollten die CGI-Programme stehen:
    #cgi_directories=['/apps']
    #Seems python 2.7 do not support sub-directory for the list
    cgi_directories=['/wwjufsdatabase/webapproot/apps','/wwjufsdatabase/webapproot/apps/collection']
    #error: ['cgi-bin'] or ['cgi-bin/']
    #correct ['/cgi-bin']
    sys.stdout.flush()
    sys.stderr.flush()


def run():
    # 8000=Port-Nummer
    # --http://localhost:8000/
    # Fuer http://localhost/
    # Port-Nummer auf 80 setzen
    #httpd = ThreadedHTTPServer(('127.0.0.1', 8802), MyRequestHandler)
    httpd=BaseHTTPServer.HTTPServer(('127.0.0.1', 8802), MyRequestHandler)
    #httpd=BaseHTTPServer.HTTPServer(('192.168.6.1', 8001), MyRequestHandler)
    #httpd=BaseHTTPServer.HTTPServer(('192.168.2.1', 8000), MyRequestHandler)
    httpd.serve_forever()

if __name__=="__main__":
    print "Starting Server"
    run()
