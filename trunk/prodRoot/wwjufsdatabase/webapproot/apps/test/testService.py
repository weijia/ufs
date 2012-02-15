#import libSys
import libs.services.services


s = libs.services.services.services()
h = s.getHtmlGen()

h.genHead()

if s.getDefaultGuestUser() == s.getUser():
    print 'not logged in'
else:
    print 'hello %s'%s.getUser()
h.genEnd()
    
