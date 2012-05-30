import Cookie
import uuid
import os
from datetime import datetime, timedelta

import localLibSys
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.http.queryParam as query

import wwjufsdatabase.libs.html.response as response
import wwjufsdatabase.libs.ufsDb.ufsDbSingleUser as dbSys
import wwjufsdatabase.libs.ufsDb.multiAccountDbSys as multiAccountDbSys
import wwjufsdatabase.libs.user.sessionV2 as sess
import wwjufsdatabase.libs.user.userManagerV2 as userMan
import localLibs.objSys.objectDatabaseV3 as objectDatabase

gSessionCookieName = "aparam"
gLoggedInNameListKeyName = u"loggedInNames"
gPrimaryLoggedInNameKeyName = u"primaryLoggedInName"
gPasswdPrefix = u"systemPass."

class ufsUser:
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd
    def getUserName(self):
        return self.username
    def getPasswd(self):
        return self.passwd

class prosedoQueryInfo:
    def __init__(self, queryInfo):
        self.queryInfo = queryInfo
    def getCookie(self):
        return {}
    def getAllFieldStorageUnicode(self):
        return self.queryInfo
    
class req:
    def __init__(self, queryInfo = None):
        if queryInfo is None:
            self.queryInfo = query.queryInfo()
        else:
            self.queryInfo = prosedoQueryInfo(queryInfo)
        self.cookie = self.queryInfo.getCookie()
        self.sysUser = ufsUser(u'system.user', u'system.pass')
        ncl(os.path.abspath(logFile))
        try:
            ncl(self.cookie)
            ncl(self.cookie[gSessionCookieName].value)
            sessionId = unicode(self.cookie[gSessionCookieName].value)
            ncl('req sessionId:'+sessionId)
        except KeyError:
            sessionId = None
        if (sessionId is None) or (sessionId.find(u':')!=-1):
            sessionId = unicode(str(uuid.uuid4()))
        ncl('sessionId:'+sessionId)
        self.session = sess.session(sessionId, dbSys.dbSysSmart(self.sysUser).getDb("sessionInfoDb"))
        self.resp = response.html()
        self.thiscookie = Cookie.SimpleCookie()
        timeoutSeconds = 60*60*24*15#15 days?
        self.thiscookie[gSessionCookieName] = sessionId
        self.thiscookie[gSessionCookieName]['path'] = '/'
        expires = datetime.utcnow() + timedelta(hours=1)
        self.thiscookie[gSessionCookieName]['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S') # Wdy, DD-Mon-YY HH:MM:SS GMT
        self.resp.setCookie(self.thiscookie)

    def getQueryInfo(self):
        return self.queryInfo
    
    def getSecondaryUsername(self):
        try:
            nameList = set(self.session[gLoggedInNameListKeyName])
        except KeyError:
            nameList = []
        return nameList
        
    def getDbSys(self):
        primaryUser = self.getPrimaryUser()
        nameList = self.getSecondaryUsername()
        try:
            nameList.remove(primaryUser.getUserName())
        except ValueError:
            pass
        userList = []
        for i in nameList:
            userList.append(ufsUser(i, self.session[gPasswdPrefix+i][0]))
            #cl(i)
        return multiAccountDbSys.dbSysSmart(primaryUser, userList, dbSys.dbSysSmart)
    
    def getObjDbSys(self, dbPrefix = "test"):
        primaryUser = self.getPrimaryUser()
        nameList = self.getSecondaryUsername()
        try:
            nameList.remove(primaryUser.getUserName())
        except ValueError:
            pass
        userList = []
        for i in nameList:
            userList.append(ufsUser(i, self.session[gPasswdPrefix+i][0]))
            #cl(i)
        u = ufsUser(primaryUser, 'nopass')
        return objectDatabase.objectDatabase(u, dbPrefix = dbPrefix)
    
    def getPrimaryUser(self):
        try:
            ncl(gPrimaryLoggedInNameKeyName)
            ncl(str(self.session[gPrimaryLoggedInNameKeyName]))
            primaryLoggedInName = self.session[gPrimaryLoggedInNameKeyName][0]
        except KeyError:
            return ufsUser(u'system.demoUser', u'system.demoUser.pass')
        return ufsUser(primaryLoggedInName, self.session[gPasswdPrefix+primaryLoggedInName][0])
        
    def verifyLogin(self):
        p = self.queryInfo.getAllFieldStorageUnicode()
        ncl(p)
        if p.has_key(u'username') and p.has_key(u'passwd'):
            username = p[u'username'][0]
            passwd = p[u'passwd'][0]
            ncl("has keys")
            if userMan.userManager().verifyPasswd(username, passwd, dbSys.dbSysSmart(self.sysUser).getDb("passwdDb")):
                ncl("login ok:"+username+","+passwd)
                self.session[gPasswdPrefix+username] = passwd
                self.session[gPrimaryLoggedInNameKeyName] = username
                ncl(str(self.session[gPrimaryLoggedInNameKeyName]))
                self.session.append(gLoggedInNameListKeyName, username)
    def setPrimaryUser(self, targetUser):
        nameList = self.getSecondaryUsername()
        if targetUser in nameList:
            self.session[gPrimaryLoggedInNameKeyName] = targetUser