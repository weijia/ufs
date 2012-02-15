import libs.html.response
import libs.platform.services
import libs.platform.ufsDbManagerInterface
import libs.tree.namedTreeItem
import libs.tree.dbTreeItem
import libs.services.nameService
try:
    import libs.user.session
    import libs.user.userManager
except:
    pass
import Cookie

class servicesInterfaceBase:
  def getQuery(self):
    pass
  def getDbMngr(self):
    pass
  def getStorage(self):
    pass
  def getHtmlGen(self):
    pass
  def getUser(self):
    pass

class servicesInterface:
  def getEncoder(self):
    pass
  def getDbMngr(self):
    pass
  def getTreeItem(self):
    pass
  def getParam(self):
    pass
  def getSimpleDb(self, dbName):
    pass
    
gGuestUser = 'richard.tester'

gLoginUsernameParamName = 'username'
gLoginPasswordParamName = 'passwd'
gDefaultSessionIdParamName = 'sessionId'


class notAuthorized:
    pass

class services:
  def __init__(self):
    self.queryInfo = libs.platform.services.getQueryService()
    self.session = None
    self.htmlGen = None
    self.requestQueryFields = self.queryInfo.getAllFieldStorage()
    self.user = None
    self.field = self.requestQueryFields
    self.mngr = None
    self.user = self.getUser()

  def getDefaultGuestUser(self):
    return gGuestUser
  def getDefaultLoginUsernameParamName(self):
    return gLoginUsernameParamName
  def getDefaultLoginPasswordParamName(self):
    return gLoginPasswordParamName
  def getSession(self):
    self.getHtmlGenManualCookie().logS('getSession called')
    if self.session is None:
      if self.getQuery().has_key(gDefaultSessionIdParamName):
        self.getHtmlGenManualCookie().logS('sid in query')
        self.session = libs.platform.services.getSession(self.getQuery()[gDefaultSessionIdParamName], self.getHtmlGenManualCookie())
      elif self.queryInfo.getCookie().has_key(gDefaultSessionIdParamName):
        self.getHtmlGenManualCookie().logS('sid in cookie:%s,%s'%(self.queryInfo.getCookie(),self.queryInfo.getCookie()[gDefaultSessionIdParamName].value))
        self.session = libs.platform.services.getSession(self.queryInfo.getCookie()[gDefaultSessionIdParamName].value, self.getHtmlGenManualCookie())
        self.getHtmlGenManualCookie().logS('sid is:%s'%self.session.getSessionId())
      else:
        self.getHtmlGenManualCookie().logS('sid not there')
        self.session = libs.platform.services.getSession(logger = self.getHtmlGenManualCookie())
    self.getHtmlGenManualCookie().logS('user name is:'+str(self.session.getValue(self.session.getDefaultSessionUsernameAttr())))
    return self.session
  def login(self):
      s = self.getSession()
      if self.getQuery().has_key(gLoginUsernameParamName) and self.getQuery().has_key(gLoginPasswordParamName):
          #To enable google account, forbiden @ in manual login account
          if self.getQuery()[gLoginUsernameParamName][0].find('@') != -1:
              raise notAuthorized()
          s.login(self.getQuery()[gLoginUsernameParamName][0],self.getQuery()[gLoginPasswordParamName][0])
      else:
          from google.appengine.api import users
          s.login(users.get_current_user().nickname(),users.get_current_user().nickname())
      self.user = s.getValue(s.getDefaultSessionUsernameAttr())

  def getUserGenException(self):
    try:
        if self.user is None:
          #First get user from session
          self.login()
          self.user = self.getSession().getValue(self.getSession().getDefaultSessionUsernameAttr())
        return self.user
    except libs.user.userManager.notAuthorized:
        raise notAuthorized()
  def getUser(self):
    try:
        return self.getUserGenException()
    except libs.user.userManager.notAuthorized:
        #print 'exception occur'
        return self.getDefaultGuestUser()
        
  def getUserAutoRedirect(self, url):
    try:
        user = self.getUserGenException()
    except libs.user.userManager.notAuthorized:
        print 'exception occur'
        pass
    if user is None:
        self.getHtmlGenManualCookie().loginAndRedirect(url)
    return user
        
  def getUserInst(self):
    return libs.platform.ufsDbManagerInterface.ufsUserExample(self.getUser())
  def getQuery(self):
    return self.field
    
  def getEncoder(self):
    en = libs.platform.services.getEncodingService()
    return en
  def getHtmlGen(self):
    h = self.getHtmlGenManualCookie()
    s = self.getSession()
    h.logS('sessionId:'+s.getSessionId())
    c = Cookie.SimpleCookie()
    c[gDefaultSessionIdParamName] = s.getSessionId()
    c[gDefaultSessionIdParamName]['max-age'] = 14*24*60*60
    c[gDefaultSessionIdParamName]['path'] = '/'
    h.setCookie(c)
    return h
  def getHtmlGenManualCookie(self):
    if self.htmlGen is None:
      self.htmlGen = libs.html.response.html()
    return self.htmlGen
    
  def getHtmlGenWithoutCookie(self):
    return self.getHtmlGenManualCookie()
    
  def getDbMngr(self):
    if self.mngr is None:
        self.mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()
    return self.mngr
  def getStorage(self, storageDbName):
    if self.getUser() is None:
      return None
    u = libs.platform.ufsDbManagerInterface.ufsUserExample(self.user)
    d = self.getDbMngr().getStorageDb(u, storageDbName)
    return d
    
  def getSysSimpleDb(self, dbName):
    u = libs.platform.ufsDbManagerInterface.ufsUserExample('richard.system')
    mngr = self.getDbMngr()
    db = mngr.getSimpleDb(u, dbName)
    return db

  def getSimpleDb(self, dbName):
    if self.getUser() is None:
      return None
    u = libs.platform.ufsDbManagerInterface.ufsUserExample(self.user)
    mngr = self.getDbMngr()
    db = mngr.getSimpleDb(u, dbName)
    return db
  def getBigValueDb(self, dbName):
    if self.getUser() is None:
      return None
    u = libs.platform.ufsDbManagerInterface.ufsUserExample(self.user)
    mngr = self.getDbMngr()
    db = mngr.getSimpleDbWithBigValue(u, dbName)
    return db
    
  def getTreeItem(self, treeDbId, nameDbId, treeItemAbsPath, sequenceDbName):
    treeDb = self.getSimpleDb(treeDbId)
    nameDb = self.getSimpleDb(nameDbId)
    nS = libs.services.nameService.nameService(nameDb)
    bigValueDb = self.getBigValueDb(sequenceDbName)
    i = libs.tree.namedTreeItem.namedTreeItem(treeItemAbsPath, treeDb, nS, bigValueDb)
    return i
  def getDefaultTreeRoot(self):
    return libs.tree.dbTreeItem.sysGlobalTreeRoot
  def getRawParam(self, key, defaultV = None):
    if self.field.has_key(key):
        return self.field[key][0]
    else:
        return defaultV
  def getParam(self, key, defaultV = None):
    if self.field.has_key(key):
        return self.getEncoder().de(self.field[key][0])
    else:
        return defaultV
  def hasParam(self, key):
    return self.field.has_key(key)