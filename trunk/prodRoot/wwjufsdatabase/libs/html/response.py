import Cookie
import StringIO
import os



def getClientIp():
  return os.environ["REMOTE_ADDR"]

from responseBase import responseBase#,gGlobalEncoding

class html(responseBase):
    def __init__(self, perPage=20, startPage=1, cookie = None):
        responseBase.__init__(self)
        self.scriptList = []
        self.embededScript = []
        self.loadedScriptList = []

        self.logS('html generator got cookie is:'+str(cookie)+'<br/>')
        self.thiscookie = cookie
        self.htmlHead = StringIO.StringIO()
        self.displayDebug = False

    def showDict(self, d):
        for i in d.keys():
          self.write('key: %s, value: %s'%(i, d[i]))
        self.refresh()

        
    def loginAndRedirect(self, url):
        self.redirect('/apps/user/login.py?nextUrl=%s'%url)
        
    def gen_button(self, handler, value):
        self.write('<input type="button" value ="%s" onclick=\'javascript:%s;\'>'%(value, handler))

        
        
    def genForm(self, action, fields, submit = 'submit', method='POST'):
        '''
        [['t','itemName'],['a','itemText']],['h','hiddenValue']
        '''
        self.write('<form action="%s" method="%s" enctype="multipart/form-data">'%(action, method))
        for i in fields:
          value = ''
          if i[0] == 't':#Input
            if len(i)> 2:
              value = ' value="%s"'%i[2]
            self.write('<input type="input" name="%s"%s><br/>'%(i[1], value))
          elif i[0] == 'a':
            if len(i)> 2:
              value = i[2]
            self.write('<textarea name="')
            self.write(i[1])
            self.write('">')
            self.write(value)
            self.write('</textarea><br/>')
          elif i[0] == 'f':
            self.write('<input type="file" name="%s">'%i[1])
          elif i[0] == 'h':
            if len(i)> 2:
              value = i[2]
            self.write('<input type="hidden" name="%s" value="%s">'%(i[1], value))
        self.write('<input type="submit" value="%s"/>'%submit)
        self.write('</form>')

        
        
    def br(self):
        self.write('<br/>')

        
    def addExtScript(self, script):
        try:
            self.loadedScriptList.index(script)
        except:
            self.scriptList.append(script)
            self.loadedScriptList.append(script)
            
    def script(self, scriptText):
        if not (scriptText is None):
            self.embededScript.append(scriptText)
        
    def inc(self, incScript):
        self.logS('inc'+str(incScript))

        if type(incScript) is list:
            for i in incScript:
                self.addExtScript(i)
        else:
            self.addExtScript(incScript)
            
    def genHead(self, title = "", extScriptList = [], internalScript = None):
        self.title = title
        self.inc(extScriptList)
        self.script(internalScript)
        
        
    def setEncoding(self, encodingName):
        self.gGlobalEncoding = encodingName
        
    def realHtmlHead(self):
        self.headers = {'Content-Type':'%s;charset=%s'%('text/html',self.gGlobalEncoding)}
        self.outputHeaders()
        print >>self.htmlHead,'''<html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=%s">
        <title>%s</title>'''%(self.gGlobalEncoding, self.title)
        for i in self.scriptList:
            print >>self.htmlHead,'<script src="%s" type="text/javascript"></script>'%i,
        for i in self.embededScript:
            print >>self.htmlHead,'<script type="text/javascript">\n%s\n</script>'%i,
        self.loadedScriptList.extend(self.scriptList)
        self.scriptList = []
        self.embededScript = []
        print >>self.htmlHead,'''
        </head>
        <body>
        '''
        self.logS('generated html header')
        
    def genEnd(self):
        if self.displayDebug:
            self.inc(["/js/development-bundle/jquery-1.4.2.js","/js/development-bundle/ui/jquery-ui-1.8.2.custom.js"])

        self.realHtmlHead()
        #Output other things
        print self.htmlHead.getvalue(),
        if self.displayDebug:
            self.write('''<script type="text/javascript">
            $(function() {
                $("#log-dialog").dialog({ width: 600 });
            });
            </script>
            ''')
            self.write('<div id="log-dialog" title="Log Window">')
            self.write(self.log)
            self.write('</div><link type="text/css" href="/js/css/smoothness/jquery-ui-1.8.2.custom.css" rel="Stylesheet" />')
        self.end()
        print '</body>'
        print '</html>'
        
    def genTxtHead(self):
        self.headers = {'Content-Type':'%s;charset=%s'%('text/plain',self.gGlobalEncoding)}
        self.outputHeaders()
        print '\n',
        
    def genPartialHtmlHead(self):
        self.headers = {'Content-Type':'%s;charset=%s'%('text/html',self.gGlobalEncoding)}
        self.outputHeaders()
        print '\n',

    def genBinHead(self):
        self.headers = {'Content-Type':'%s'%('binary/octet-stream')}
        self.outputHeaders()
        print '\n',
        
    def genJsonHead(self):
        self.headers = {'Content-Type':'%s;charset=%s'%('application/JSON', self.gGlobalEncoding)}
        self.outputHeaders()
        print '\n',