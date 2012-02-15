try:
    import libs.GAE.ufsDbGaeTokenDb
    import libs.GAE.ufsDbGaeEntryDbV2
    import libs.ufsDb.ufsDbBase
    import libs.ufsDb.ufsDbEncryptedTokenDb
    import libs.encryption.encryptionManager
except:
    pass

sysOwnerAttr = 'sys_owner'
sysDbIdAttr = 'sys_dbId'
sysHashedPasswdAttr = 'sys_hashedPasswd'
sysEncryptedTokenPasswdAttr = 'sys_encryptedTokenPasswd'
sysSharedDbAttr = 'sys_sharedDb'

class databaseManager:

  gDefaultPasswd = 'defaultpass'
  
  def __init__(self):
    self.dbMngrDb = self.getUfsDbBase('system', 'dbMngrDb')
    self.cryptoMngr = libs.encryption.encryptionManager.encryptionManager('system', 'dbMngrDb')
    
  def getUfsDbBase(self, owner, dbId):
    t = libs.GAE.ufsDbGaeTokenDb.ufsDbGaeTokenDb(owner,dbId)
    e = libs.GAE.ufsDbGaeEntryDbV2.ufsDbGaeEntryDb(owner,dbId)
    return libs.ufsDb.ufsDbBase.ufsDbBase(t,e)

  def getUfsDb(self, owner, dbId, session, encryption = True, shared = False):
    '''
    session is used to get userMasterPassword
    '''
    #First find the records
    l = self.dbMngrDb.getObjIdListAllCondition({sysOwnerAttr:owner,sysDbIdAttr:dbId})
    if len(l) > 1:
      print 'there is more than one database using the same username and dbid'
    if len(l) == 0:
      self.createUfsDb(owner, dbId, session, encryption = True, shared = False)
    
    #Get the db obj, first check if it is encrypted
    p = self.dbMngrDb.getAttr(l[0], sysEncryptedTokenPasswdAttr)
    if p is None:
      return self.getUfsDbBase(owner, dbId)
    
    #If it is single user database, the password for token Db is encrypted using user's master password
    s = int(self.dbMngrDb.getAttr(l[0], sysSharedDbAttr))
    
    if s == 1:
      #Shared, use default passwd
      tk = self.cryptoMngr.decryption(p, self.gDefaultPasswd)
    else:
      tk = self.cryptoMngr.decryption(p, session.getMasterPasswd())
    return libs.ufsDb.ufsDbEncryptedTokenDb(owner, dbId, tk)

  def createUfsDb(self, owner, dbId, session, encryption = True, shared = False):
    '''
    session is used to get userMasterPassword
    '''
    l = self.dbMngrDb.getObjIdListAllCondition({sysOwnerAttr:owner,sysDbIdAttr:dbId})
    if len(l) > 0:
      return False
    import uuid
    dbUuid = str(uuid.uuid4())
    self.dbMngrDb.add(dbUuid, sysOwnerAttr, owner)
    self.dbMngrDb.add(dbUuid, sysDbIdAttr, dbId)
    
    if encryption:
      tokenDbKey = self.cryptoMngr.getRandomKey()
      if shared:
        tk = self.cryptoMngr.encrypt(key, self.gDefaultPasswd)
        self.dbMngrDb.add(dbUuid, sysSharedDbAttr, 1)
      else:
        tk = self.cryptoMngr.encrypt(key, session.getMasterPasswd())
        self.dbMngrDb.add(dbUuid, sysSharedDbAttr, 0)
      self.dbMngrDb.add(dbUuid, sysEncryptedTokenPasswdAttr, tk)
      
    
