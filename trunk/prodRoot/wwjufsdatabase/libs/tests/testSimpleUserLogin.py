import urllib
import libSys
import libs.html.serverResponseParser


def login(username, passwd):
  params = urllib.urlencode({'username': username, 'passwd': passwd})
  print "http://127.0.0.1:9901/apps/simpleUserLogin.py?%s" % params
  f = urllib.urlopen("http://127.0.0.1:9901/apps/simpleUserLogin.py?%s" % params,proxies = {})
  p = libs.html.serverResponseParser.serverResponseParser()
  print 'returned value-------------------------------'
  l = p.parseValueList(f)
  print l
  
  
login('test1', 'testpass')