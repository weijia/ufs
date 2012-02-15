try:
    import libs.user.session
except:
    pass
import ufsDbService
import libs.http.queryParam


class encodingSys:
  def de(self, encodedStr):
    '''
    Decode str to unicode from client
    '''
    return encodedStr.decode('utf-8')
  def en(self, decodedStr):
    return decodedStr.encode('utf-8')

class serviceProvider:
  def __init__(self):
    self.currentSession = None
    self.currentQuery = None
    
  def getSession(self, sid = None, logger = None):
    #if self.currentSession is None:
    if True:
      db = mngr.getSystemSimpleDb('sessionDb')
      #print 'service got sid is:',sid
      self.currentSession = libs.user.session.session(db, sid, logger)
    return self.currentSession
    
    
  def getQueryService(self):
    #if self.currentQuery is None:
    if True:
      self.currentQuery = libs.http.queryParam.queryInfo()
      #print 'query info created'
    return self.currentQuery



currentServiceProvider = serviceProvider()

def getEncodingService():
  return encodingSys()
  
def getSession(sid = None, logger = None):
  global currentServiceProvider
  return currentServiceProvider.getSession(sid, logger)
  
  
def getQueryService():
  global currentServiceProvider
  return currentServiceProvider.getQueryService()
  
  
class login_required(object):
  def __init__(self, f):
    self.f = f
  def __call__(self, session):
    if session.getValue('system.user') is None:
      return False
    self.f(session)
    
    
    
