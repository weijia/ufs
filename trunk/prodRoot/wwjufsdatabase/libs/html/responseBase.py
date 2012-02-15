import StringIO
import sys
import libSys
import libs.utils.encodingTools as encodingTools
import localLibSys
from localLibs.logSys.logSys import *
#gGlobalEncoding = 'gbk'

class responseBaseInterface:
    def __init__(self):
        pass
    def end(self):
        '''
        Called whenever the page is txt or html
        '''
        pass
class responseBase(responseBaseInterface):
    def __init__(self):
        #self.headers = {'Content-Type':'%s;charset=%s'%('text/html','utf-8')}
        self.headers = {}
        self.out = ''
        self.log = ''
        self.htmlHead = ''
        self.gGlobalEncoding = encodingTools.getPageEncoding()
        
    def logS(self, s):
        import cgi
        self.log += cgi.escape(s)+'<br/>--------------------------------------------<br/>'
    def outputHeaders(self):
        cl('outputHeaders')
        cl(self.thiscookie)
        #Output headers
        for i in self.headers.keys():
            print i,':',self.headers[i],'\n',
        if not (self.thiscookie is None):
            print self.thiscookie,'\n',
        else:
            print '\n',

    def end(self):
        #Output other things
        sys.stdout.write(self.out)

    def write(self, o):
        self.out += o.encode(self.gGlobalEncoding, 'xmlcharrefreplace')
        #self.out += o.encode(self.gGlobalEncoding, 'backslashreplace')

    def setCookie(self, cookie):
        cl('setting cookie to:%s'%str(cookie))
        self.thiscookie = cookie

        
        
    def redirect(self, url):
        self.write('redirecting to:%s'%url)
        self.write('''
        <script type="text/javascript">
        document.location.href="%s";
        </script>
        '''%url)
