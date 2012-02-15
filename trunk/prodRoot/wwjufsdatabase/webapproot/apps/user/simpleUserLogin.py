#import libs.GAE.session
#import libs.http.queryParam
import libs.platform.services


q = libs.platform.services.getQueryService()
f = q.getGetFieldStorage()
#print f['sessionId']
#print f['sessionId'][0]

print "Content-Type: text/html;charset=utf-8"
print ""
print f
if f.has_key('sessionId'):
  sid = f['sessionId'][0]
else:
  sid = None
print 'sid got from url:',sid
s = libs.platform.services.getSession(sid)

s.login(f['username'][0], f['passwd'][0])
#print 'session id is: ',s.uid
print 'session uid is: ',s.uid
print 'session key: user is:', s.getValue('user')
print '\'\'\'\'----------------'
print 'OK'
print s.uid