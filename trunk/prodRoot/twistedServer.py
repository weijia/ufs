#!/usr/bin/env python
import sys
from CGIHTTPServer import CGIHTTPRequestHandler
import BaseHTTPServer
'''
import urlparse
import posixpath
import urllib
import os
'''

import sys
sys.path.insert(0, 'app')
import configuration

class MyRequestHandler(CGIHTTPRequestHandler):
    # In diesem Verzeichnis sollten die CGI-Programme stehen:
    cgi_directories=["/app","/webapproot/apps"]
    #error: ['cgi-bin'] or ['cgi-bin/']
    #correct ['/cgi-bin']
    
    def run_cgi(self):
        sys.stderr.flush()
        CGIHTTPRequestHandler.run_cgi(self)
    
'''
class logSys:
    def __init__(self):
        self.console = sys.stdout
        self.consoleErr = sys.stderr
        sys.stdout = open('d:/out.txt','w')
        #sys.stderr = open('d:/erro.txt','w')
        sys.stderr = self

    def write(self, data):
        print >>self.console, 'write called:%s'%data
        pass

def run():
    # 8000=Port-Nummer
    # --http://localhost:8000/
    # Fuer http://localhost/
    # Port-Nummer auf 80 setzen
    #log = logSys()
    httpd=BaseHTTPServer.HTTPServer(('127.0.0.1', 8801), MyRequestHandler)
    #httpd=BaseHTTPServer.HTTPServer(('192.168.2.1', 8000), MyRequestHandler)
    httpd.serve_forever()
'''


from twisted.internet import reactor
from twisted.web import static, server, twcgi
from twisted.web.resource import Resource
#from dbXmlRpcServer import *

       
class PythonScript(twcgi.FilteredScript):
  filter = 'c:\\Python25\\python.exe'

def run():
  root = static.File('./')
  #root.putChild('', Collection())
  #root.putChild('', static.File('./'))
  #root.putChild('img', static.File('./img'))
  #root.putChild('app', twcgi.CGIDirectory('./app'))
  #There is default processor, so we don't need to add new one 
  root.processors = {'.py': PythonScript}
  #root.putChild('app', static.File('./app'))
  reactor.listenTCP(configuration.g_default_webserver_port, server.Site(root))
  #r = dbXmlRpcServer()
  #reactor.listenTCP(configuration.g_default_xmlrpc_port, server.Site(r))
  reactor.run()



if __name__=="__main__":
    print "Starting Server twisted"
    run()
