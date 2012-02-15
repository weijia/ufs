import urllib
import libSys
import libs.html.serverResponseParser



class ufsClient:
  def __init__(self):
    self.loggedIn = False
    self.sid = None
  def login(self, username, passwd):
    if not self.loggedIn:
      params = urllib.urlencode({'username': username, 'passwd': passwd})
      print "http://127.0.0.1:9901/apps/simpleUserLogin.py?%s" % params
      f = urllib.urlopen("http://127.0.0.1:9901/apps/simpleUserLogin.py?%s" % params,proxies = {})
      p = libs.html.serverResponseParser.serverResponseParser()
      print 'returned value-------------------------------'
      l = p.parseValueList(f)
      print l
      if l[0] == 'OK':
        self.loggedIn = True
        self.sid = l[1]
  # def postRequest(self, url, ufsPostData):
    # if self.loggedIn:
      # e = urllib.urlencode('ufsPostData':ufsPostData, 'uuid',str(self.sid))
      # f = urllib.urlopen(url,proxies = {},data=e)
      # p = libs.html.serverResponseParser.serverResponseParser()
      # print 'returned value-------------------------------'
      # l = p.parseValueList(f)
      # print l
    # else:
      # raise 'Please log in first'

  def getSessionId(self):
    if self.loggedIn:
      return self.sid
    else:
      raise 'Please login first'