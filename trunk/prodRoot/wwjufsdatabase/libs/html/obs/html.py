import os
import urllib
from shove import Shove

sessionList = Shove('sqlite:///session.sqlite', 'sqlite:///cache.sqlite')

from logSys import *
gPostStringVar = None

#create logger
logger = logging.getLogger("htmlLogger")

def gen_button(handler, value):
  print '<input type="button" value ="%s" onclick=\'javascript:%s;\'>'%(value, handler)

def trans(data):
    try:
        de = data.decode('gb2312')
        #print 'gb2312 encoded'
        #print de
        return de
    except:
        #print 'other encoded'
        return data

def listParamCallback(ret, key, value):
    if ret.has_key(key):
        if type(ret[key]) == list:
            ret[key].append(value)
        else:
            ret[key] = value
    else:
        ret[key] = []
        ret[key].append(value)

def singleParamCallback(ret, key, value):
    ret[key] = value

'''
when posted, ' ' will be replaced to '+', so here '+' should be replalced by ' '
& will be the spliter
'''

def parseParam(qstr, callbackFunc):
  ret = {}
  qstr = qstr.replace('+', ' ')
  #split out the url part and param part? No need, the url part is alrady removed
  params = qstr.split('&')
  for p in params:
    #if the client is a chinese client, and the url is input by hand in url bar,
    #the url will be encoded in 'gb2312'. so it may need encode again
    pair = p.split('=')
    paramKey = trans(urllib.unquote(pair[0]))
    if len(pair) < 2:
      value = ''
    else:
      value = trans(urllib.unquote(pair[1]))
    callbackFunc(ret, paramKey, value)
  return ret
    
def getParamPairsFromStrInList(qstr):
  '''
  This function will return a list of value for each key.
  '''
  ret = parseParam(qstr, listParamCallback)
  return ret

def getParamPairsFromStr(qstr):
  '''
  This function will return a value for each key
  '''
  ret = parseParam(qstr, singleParamCallback)
  return ret


def getGetParamPairs(genFunc = getParamPairsFromStr):
    qstr = os.environ.get('QUERY_STRING','')
    #print qstr
    ncl(qstr)
    if qstr != '':
        pa = genFunc(qstr)
        ncl(pa)
        return pa
    else:
        return {}

def getPostParamPairs(genFunc = getParamPairsFromStr):
    global gPostStringVar
    if gPostStringVar == None:
      gPostStringVar = sys.stdin.readlines()
    '''
    for i in lines:
        print i
    '''
    return genFunc(''.join(gPostStringVar))

def getParamPairsAll():
    ret1 = getPostParamPairs()
    #print ret1
    ret1.update(getGetParamPairs())
    #print ret1
    return ret1

def getParamPairsAllInList():
    ret1 = getPostParamPairs(getParamPairsFromStrInList)
    #print ret1
    ret1.update(getGetParamPairs(getParamPairsFromStrInList))
    #print ret1
    return ret1

def getParamPairs():
    return getParamPairsAll()

def getParamPairsInList():
    return getGetParamPairs(getParamPairsFromStrInList)


def buildParams(paramDic):
    paramList = []
    for i in paramDic.keys():
        if type(paramDic[i]) == list:
            paramList.append('%s=%s'%(i,urllib.quote(','.join(paramDic[i]))))
        else:
            paramList.append('%s=%s'%(i,urllib.quote(str(paramDic[i]))))
    return '&'.join(paramList)


class html:
    def __init__(self, perPage=20, startPage=1):
        self.perPage = perPage
        self.startPage = startPage
        self.pa = getParamPairsAll()

        if self.pa.has_key('pageNum'):
            self.startPage = int(self.pa['pageNum'])
        else:
            self.pa['pageNum'] = self.startPage
        
        if self.pa.has_key('perPage'):
            self.perPage = int(self.pa['perPage'])
        else:
            self.pa['perPage'] = self.perPage
        global gPostStringVar
        self.initSession()

        
        
        
    def initSession(self):
        timeoutSeconds = 60*30*60#30 min?
        import uuid
        import time
        #Get session id or generate one
        import os
        import Cookie
        self.thiscookie = Cookie.SimpleCookie()
        #cl('init session')
        if os.environ.has_key('HTTP_COOKIE'):
          self.thiscookie.load(os.environ['HTTP_COOKIE'])
          #cl('cookie:',thiscookie['aparam'].value)
          #print thiscookie['aparam']
          self.sessionid = self.thiscookie['aparam'].value
          try:
            test = sessionList[self.sessionid]['refreshedTime']
          except KeyError:
            #self.showDict(sessionList)
            #cl('sessionid is not in sessionList')
            test = None
            
          if test is None:
            pass
          else:
            if time.time() - sessionList[self.sessionid]['refreshedTime'] < timeoutSeconds:
              #Timeout not reached
              #cl('sessionid is not in sessionList')
              return
        if self.pa.has_key('sessionid'):
            #cl('has key')
            self.sessionid = self.pa['sessionid']
            #Check session timeout
            if time.time() - sessionList[self.sessionid]['refreshedTime'] < timeoutSeconds:
                #Session is not timeout
                #cl('initSession: session is not out')
                return
            else:
                pass
                #cl('timeout reached')
                #cl(time.time() -sessionList[self.sessionid]['refreshedTime'], timeoutSeconds)
        #cl('generating new uuid')
        self.sessionid = str(uuid.uuid4())
        #cl('session is:',self.sessionid)
        sessionData = {}
        sessionData['refreshedTime'] = time.time()
        sessionList[self.sessionid] = sessionData
        self.pa['sessionid'] = self.sessionid
        self.thiscookie = Cookie.SimpleCookie()
        self.thiscookie['aparam'] = self.sessionid
        self.thiscookie['aparam']['max-age'] = timeoutSeconds
        #print thiscookie['aparam']
        #The following print is necessary. It will send cookie to client.
        #print self.thiscookie
    def showSessionInfo(self):
        self.showDict(sessionList[self.sessionid])
    def showDict(self, d):
        for i in d.keys():
          print 'key: %s, value: %s'%(i, d[i])     
    def showParmas(self):
        self.showDict(self.pa)
    def addSessionInfo(self, key, value):
        '''
        This function must reassign the dict object in sessionList. Otherwise, the dict in sessionList is not updated.
        '''
        o = sessionList[self.sessionid]
        o[key] = value
        sessionList[self.sessionid] = o
        #sessionList[self.sessionid][key] = value
        #print '------------------------adding session data',key, value,'<br/>'
        #self.showSessionInfo()
    def getSessionInfo(self, key):
        return sessionList[self.sessionid][key]
    def genHead(self, title = ""):
        '''
        output will first handled by outReceived in  twisted/web/twcgi.py
        '''
        #print self.thiscookie
        #Do not edit the following string without understanding the line end schema. Please use the same line end schema. For example,
        #Use only \n as line terminator
        print "Content-Type: text/html;charset=utf-8\n%s\n\n"%self.thiscookie
        #print self.thiscookie
        print '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=windows-1250">
        <title>
        '''
        print title
        print '''</title>
        </head>
        '''
        print self.sessionid
        print sessionList[self.sessionid]
        #self.headSent = True
        #cl(gPostStringVar)
    def genPageInfo(self):
        #start = pa['start']#Item indexed from 1
        if int(self.startPage) > 1:
            self.pa['pageNum'] = int(self.startPage) - 1
            print '<a href='+os.environ.get('SCRIPT_FILE','')+ \
                '?%s>previous page</a>'%(buildParams(self.pa))
        self.pa['pageNum'] = int(self.startPage) + 1
        print '<a href='+os.environ.get('SCRIPT_FILE','')+ \
            '?%s>next page</a>'%(buildParams(self.pa))
        self.pa['pageNum'] = int(self.startPage)
    def getStartItemCount(self):
        return self.perPage*(self.startPage-1)
    def getLimit(self):
        return self.perPage
    def getParams(self):
        return self.pa
    def genEnd(self):
        print '</html>'
    def redirect(self, url):
        print '''
        <script>
        document.location.href="%s";
        </script>
        '''%url
    def gen_button(self, handler, value):
        print '<input type="button" value ="%s" onclick=\'javascript:%s;\'>'%(value, handler)
      
from tableOutput import *
def outputParams():
    print '---------------------------post<br/>'
    lines = sys.stdin.readlines()
    for i in lines:
        print i
    
    print '<br/>---------------------------post decoded<br/>'
    
    pa = getParamPairsFromStrInList(''.join(lines))
    
    for i in pa.keys():
        print i,'=',pa[i]
    
    print '<br/>----------------------------get<br/>'
    
    qstr = os.environ.get('QUERY_STRING','')
    
    print qstr
    print '<br/>'
    pa = getParamPairs()
    for i in pa.keys():
        print i,'=',pa[i],'<br/>'
