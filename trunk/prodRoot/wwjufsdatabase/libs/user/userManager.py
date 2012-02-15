
from google.appengine.ext import db
import md5
import libs.encryption.encryptionManager

class userDbInterface:
  def login(self, user, password):
    pass
  def validate(self, uid):
    pass
  def getValue(self, uid, key):
    pass
  def setValue(self, uid, key, value):
    pass
    
gUserDbVersion = 1

class notAuthorized:
    pass

class userInfo(db.Model):
  #user name for this entry
  user = db.StringProperty(required=True)
  hashedPass = db.StringProperty(required=True)
  encryptedUserMasterPasswd = db.StringProperty(required=True)
  createdData = db.DateTimeProperty(auto_now_add=True)
  version = db.IntegerProperty()

class userDbGAE(userDbInterface):
  def __init__(self, user = None, password = None):
    self.cryptoMngr = libs.encryption.encryptionManager.encryptionManager('system', 'userMngr')
    if (user is None) or (password is None):
      self.loginFlag = False
    else:
      self.loginFlag = self.login(user, password)
  def login(self, user, password):
    u = self.getUser(user)
    k = self.cryptoMngr.getRandomKey()
    if u is None:
      #User does not exist, create it.
      u = userInfo(
        user = user,
        hashedPass = str(md5.new(password).hexdigest()),
        encryptedUserMasterPasswd = self.cryptoMngr.encrypt(k, password),
        version = gUserDbVersion
      )
      u.put()
      return True
    else:
      if u.hashedPass == str(md5.new(password).hexdigest()):
        return True
      else:
        raise notAuthorized()
  def getUser(self, user):
    q = db.GqlQuery("SELECT * FROM userInfo " +
                "WHERE user = :1 " +
                "ORDER BY __key__",
                user)

    results = q.fetch(5)
    for p in results:
      return p
    return None
  def getMasterPasswd(self, user, password):
    u = self.getUser(user)
    if u is None:
      raise 'no such user'
    else:
      if u.hashedPass == str(md5.new(password).hexdigest()):
        return self.cryptoMngr.encrypt(u.encryptedUserMasterPasswd, password)
    return None
  '''
  def validate(self, uid):
    pass
  def getValue(self, uid, key):
    pass
  def setValue(self, uid, key, value):
    pass
  '''