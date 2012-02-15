'''
Session contains data that will be discarded after some period of time.
'''
sessionExpireTime = 18000

class sessionInterface:
  def __init__(self, uid):
    pass
  def getValue(key):
    pass
  def setValue(key, value):
    pass
    
from google.appengine.api import memcache
#from google.appengine.ext import db

import uuid
import userManager

'''
class sessionInfo(db.Model):
  uid = db.StringProperty(required=True)
  key = db.StringProperty(required=True)
  value = db.StringProperty(required=True)
  createdData = db.DateTimeProperty(auto_now_add=True)
  version = db.IntegerProperty()

'''
import libs.html.response

gSessionUsernameAttr = 'richard.session.username'
#gDefaultSessionIdAttr = 'richard.session.sid'

class session:
  def __init__(self, ufsBaseDbInstance, sid = None, logger = None):
    self.logger = logger
    self.logS('creating session, initial sid:%s'%sid)
    # Add a value if it doesn't exist in the cache, with a cache expiration of sessionExpireTime seconds.
    ip = libs.html.response.getClientIp()
    try:
      if memcache.get(sid) != ip:
        sid = str(uuid.uuid4())
        self.logS('different ip with same sid')
    except:
      sid = str(uuid.uuid4())
      self.logS('new sid')
    memcache.add(key=sid, value=ip, time=sessionExpireTime)
    self.sid = sid
    self.uM = userManager.userDbGAE()
    self.db = ufsBaseDbInstance
  def setLogger(self, logger):
    self.logger = logger
  def logS(self, s):
    if not (self.logger is None):
        self.logger.logS(s)
  def login(self, user, passwd):
    if not (self.getValue(gSessionUsernameAttr) is None):
      return
    if self.uM.login(user, passwd):
      #Added user name to session value
      self.setValue(gSessionUsernameAttr,user)
      #print 'login ok, user is:',user
      #Added user master passwd to session value
      self.setValue('userMasterPasswd', self.uM.getMasterPasswd(user, passwd))
  def getValue(self, key):
    #print 'getting value for sid:', self.sid
    i = self.db.getAttr(self.sid, key)
    return i
  def setValue(self, key, value):
    #print 'setting value for sid:', self.sid
    self.db.add(self.sid, key, value)

  def getDefaultSessionUsernameAttr(self):
    return gSessionUsernameAttr
  def getSessionId(self):
    return self.sid