#import libs.GAE.session
import libs.http.queryParam
import libs.platform.services
import urllib

def decode(s):
  try:
    return s.decode('gb2312')
  except:
    pass
  return s

@login_required
def handleUfsWebDbRequest(cgiService):
  q = cgiService.getQueryService()
  l = q.getPostData().split('\n')
  
  s = q.getSession()
  dbId = s.getValue('curDbId')
  ownerId = s.getValue('ownerId')
  if dbId is None or ownerId is None:
    return False
  db = ufsDbService.getUfsDb(ownerId, dbId, s)
  if db is None:
    return False
  for i in l:
    i = i.replace('\r','').replace('\n','')
    if i == '':
      continue
    op, k = i.split('?',1)
    if op == 'add':
      params = k.split('&')
      ret = {}
      for p in params:
        #if the client is a chinese client, and the url is input by hand in url bar,
        #the url will be encoded in 'gb2312'. so it may need encode again
        ke,ve = p.split('=',1)
        k = decode(ke)
        v = decode(ve)
        ret[k] = v
      db.add(ret['uuid'], ret['key'], ret['value'], ret['app'])
  return True
      
print "Content-Type: text/html;charset=utf-8"
print ""

s = libs.platform.services.getSession()
q = libs.platform.services.getQueryService()
g = q.getGetFieldStorage()
dbId = g['curDbId'].value
s.setValue('curDbId', )
handleUfsWebDbRequest(s)