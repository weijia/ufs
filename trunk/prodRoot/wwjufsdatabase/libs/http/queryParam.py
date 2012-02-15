import cgi
import sys
import os
import StringIO
import libSys
import libs.utils.encodingTools as encodingTools
import localLibSys
from localLibs.logSys.logSys import *

def getClientIp():
    return os.environ["REMOTE_ADDR"]

def isLocal():
    try:
        getClientIp()
        return False
    except KeyError:
        return True

def decode(s):
    try:
        return s.decode('utf8')
    except:
        return s.decode('gbk')

class queryInfo:
    def __init__(self):
        self.httpPostData = None#Post data
        self.httpFieldData = None#All data in hash table
        self.getDataFlag = False
        self.postDataFlag = False
        self.cookies = None
        self.unicodeFieldData = {}
    
    def getPostData(self):
        if self.httpPostData is None:
            self.httpPostData = sys.stdin.read()
        return self.httpPostData
    def getAllFieldStorage(self):
        '''
        Get the fields in URL and POST
        '''
        #print 'getAllFieldStorage called'
        self.getPostData()
        if self.httpFieldData is None:
            s = StringIO.StringIO(self.httpPostData)
            self.httpFieldData = cgi.parse(s)
            #print 'first return:', self.httpFieldData
            #The following is not needed as the parse function will automatically include query string
            #s = StringIO.StringIO(os.environ.get('QUERY_STRING',''))
            #self.httpFieldData = cgi.parse(s)
            #print 'second return:',self.httpFieldData
            for i in self.httpFieldData:
                r = []
                for j in self.httpFieldData[i]:
                    r.append(decode(j))
                self.unicodeFieldData[i.decode(encodingTools.getPageEncoding())] = r
            self.postDataFlag = True
        return self.httpFieldData
    def getAllFieldStorageUnicode(self):
        self.getAllFieldStorage()
        return self.unicodeFieldData
    def getGetFieldStorage(self):
        '''
        Only get the fields sent in URL
        '''
        if self.httpFieldData is None:
            #print 'environment:',os.environ.get('QUERY_STRING','')
            s = StringIO.StringIO('')
            self.httpFieldData = cgi.parse(s)
            #print 'first return:', self.httpFieldData
            self.getDataFlag = True
        return self.httpFieldData
    
    def getCookie(self):
        import Cookie
        if self.cookies is None:
            self.cookies = Cookie.SimpleCookie()
            self.cookieDict = {}
            try:
                cl(os.environ["HTTP_COOKIE"])
                self.cookies.load(os.environ["HTTP_COOKIE"])
                '''
                for key, value in self.cookies.items():
                    self.cookieDict[key] = value.value
                '''
            except KeyError:
                pass
        return self.cookies
    