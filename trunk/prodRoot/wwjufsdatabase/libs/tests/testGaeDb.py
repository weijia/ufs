from libs.GAE import ufsDbGaeEntryDb, ufsDbGaeTokenDb
#import libs.GAE.session as session#This can not work.
from libs.ufsDb import ufsDbBase


td = ufsDbGaeTokenDb.ufsDbGaeTokenDb('testtoken','testtoken')
ed = ufsDbGaeEntryDb.ufsDbGaeEntryDb('testentry','testentry')
d = ufsDbBase.ufsDbBase(td, ed)
d.add('abcid', 'abck', 'abcv', 'abcapp')
from google.appengine.ext import db

print "Content-Type: text/plain"
print ""
q = db.GqlQuery("SELECT * FROM ufsEntry " +
            "WHERE owner = :1 AND dbId = :2 " +
            "ORDER BY __key__",
            'testentry', 'testentry')

results = q.fetch(5)
for p in results:
  print p.objId, p.keyId, p.valueId
