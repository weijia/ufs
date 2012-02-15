import Cookie
import StringIO
import os

def getClientIp():
  return os.environ["REMOTE_ADDR"]


class html:
    def __init__(self, perPage=20, startPage=1, cookie = None):
        self.headFlag = False
        self.out = StringIO.StringIO()
        self.scriptList = []
        self.embededScript = []
        self.loadedScriptList = []

        self.refreshFlag = True
        self.log = 'html generator got cookie is:'+str(cookie)+'<br/>'
        if cookie is None:
            self.thiscookie = Cookie.SimpleCookie()
        else:
            self.thiscookie = cookie
    def showDict(self, d):
        for i in d.keys():
          print >>self.out,'key: %s, value: %s'%(i, d[i])     
        self.refresh()
    def genTxtHead(self):
        print >>self.out,"Content-Type: text/plain;charset=utf-8\n\n",
        self.refresh()
    def setCookie(self, cookie):
        self.logS('setting cookie to:%s'%str(cookie))
        self.thiscookie = cookie
    def genScript(self):
        self.logS(str(self.scriptList))
        self.logS(str(self.embededScript))
        for i in self.scriptList:
            print >>self.out,'<script src="%s" type="text/javascript"></script>'%i
        for i in self.embededScript:
            print >>self.out,'<script type="text/javascript">\n%s\n</script>'%i
        self.scriptList = []
        self.embededScript = []

    def genHead(self, title = "", extScriptList = [], internalScript = None):
        '''
        out will first handled by outReceived in  twisted/web/twcgi.py
        '''
        if self.headFlag:
          return
        else:
          self.headFlag = True
        #print self.thiscookie
        #Do not edit the following string without understanding the line end schema. Please use the same line end schema. For example,
        #Use only \n as line terminator
        #print >>self.out,"Content-Type: text/html;charset=utf-8\n%s\n"%self.thiscookie
        print >>self.out,"Content-Type: text/html;charset=utf-8\n%s\n"%self.thiscookie
        self.logS(str(self.thiscookie))
        print >>self.out,'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">',
        print >>self.out,'''<html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <title>
        '''
        print >>self.out,title
        print >>self.out,'''</title>'''
        self.inc(extScriptList)
        #self.genScript()
        if not (internalScript is None):
            print >>self.out,'<script type="text/javascript">%s</script>'%internalScript
        self.logS(self.out.getvalue())
        print >>self.out,'''
        </head>
        '''
        #self.headSent = True
        #cl(gPostStringVar)
        #print >>self.out,self.thiscookie
        #self.logS(self.out.getvalue())
        self.logS('generated html header')
        self.refresh()
        
    def genEnd(self):
        for i in self.scriptList:
            print '<script src="%s" type="text/javascript"></script>'%i,
        for i in self.embededScript:
            print '<script type="text/javascript">\n%s\n</script>'%i,
        self.scriptList = []
        self.embededScript = []
        self.realOut()
        if True:
            print '<script src="%s" type="text/javascript"></script>'%"/js/development-bundle/jquery-1.4.2.js"
            print '''<script type="text/javascript">
	$(function() {
		$("#log-dialog").dialog({ width: 600 });
	});
	</script>
    '''
            print '<div id="log-dialog" title="Log Window">'
            print self.log
            print '</div><script src="/js/development-bundle/ui/jquery-ui-1.8.2.custom.js" type="text/javascript"></script><link type="text/css" href="/js/css/smoothness/jquery-ui-1.8.2.custom.css" rel="Stylesheet" />'
        print '</body>'
        print '</html>'
        
    def redirect(self, url):
        print >>self.out,'redirecting to:%s'%url
        print >>self.out,'''
        <script type="text/javascript">
        document.location.href="%s";
        </script>
        '''%url
        self.refresh()
        
    def loginAndRedirect(self, url):
        self.redirect('/apps/user/login.py?nextUrl=%s'%url)
    def gen_button(self, handler, value):
        print >>self.out,'<input type="button" value ="%s" onclick=\'javascript:%s;\'>'%(value, handler)
        self.refresh()
        
        
    def genForm(self, action, fields, submit = 'submit', method='POST'):
        '''
        [['t','itemName'],['a','itemText']],['h','hiddenValue']
        '''
        print >>self.out,'<form action="%s" method="%s" enctype="multipart/form-data">'%(action, method)
        for i in fields:
          value = ''
          if i[0] == 't':#Input
            if len(i)> 2:
              value = ' value="%s"'%i[2]
            print >>self.out,'<input type="input" name="%s"%s><br/>'%(i[1], value)
          elif i[0] == 'a':
            if len(i)> 2:
              value = i[2]
            print >>self.out,'<textarea name="%s">%s</textarea><br/>'%(i[1], value)
          elif i[0] == 'f':
            print >>self.out,'<input type="file" name="%s">'%i[1]
          elif i[0] == 'h':
            if len(i)> 2:
              value = i[2]
            print >>self.out,'<input type="hidden" name="%s" value="%s">'%(i[1], value)
        print >>self.out,'<input type="submit" value="%s"/>'%submit
        print >>self.out,'</form>'
        self.refresh()
        
        
    def br(self):
        print >>self.out,'<br/>'
        self.refresh()
    def addExtScript(self, script):
        try:
            self.loadedScriptList.index(script)
        except:
            self.scriptList.append(script)
            self.loadedScriptList.append(script)
    def inc(self, incScript):
        self.logS('inc'+str(incScript))
        #self.refreshFlag = False
        if type(incScript) is list:
            for i in incScript:
                self.addExtScript(i)
        else:
            self.addExtScript(incScript)
        self.refresh()
    def script(self, scriptText):
        self.embededScript.append(scriptText)
    def refresh(self):
        if self.refreshFlag:
            self.realOut()
    def realOut(self):
        self.genScript()
        print self.out.getvalue(),
        
        self.out = StringIO.StringIO('')
    def write(self, o):
        #self.refreshFlag = False
        self.out.write(o)
        self.refresh()
    def end(self):
        self.refreshFlag = True
        self.refresh()
        print self.log
    def logS(self, s):
        import cgi
        self.log += cgi.escape(s)+'<br/>--------------------------------------------<br/>'
    def newStyle(self):
        self.refreshFlag = False