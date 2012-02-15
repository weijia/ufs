#import libs.GAE.session
import libs.http.queryParam
import libs.platform.services
import libs.platform.ufsDbManagerInterface

print "Content-Type: text/html;charset=utf-8"
print ""

q = libs.platform.services.getQueryService()
f = q.getAllFieldStorage()
#print f['sessionId']
#print f['sessionId'][0]

if f.has_key('sessionId'):
  sid = f['sessionId'][0]
else:
  sid = None
print 'sid got from url:',sid
s = libs.platform.services.getSession(sid)

u = libs.platform.ufsDbManagerInterface.ufsUserExample(s.getValue('user'))
mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

import urllib
dbHash = {}

qsl = f['operationData']

for qs in qsl:
  qll = qs.split('\n')
  for ql in qll:
    if ql.split('?')[0] == 'add':
      p = ql.split('?')[1].split('&')
      dbName = urllib.unquote(p[0].split('=')[1])
      key = urllib.unquote(p[1].split('=')[1])
      value = urllib.unquote(p[2].split('=')[1])
      createapp = urllib.unquote(p[3].split('=')[1])
      if not dbHash.has_key(dbName):
        dbHash[dbName] = mngr.getStorageDb(u, dbName)
      dbHash[dbName].storeData(key, value, createapp)