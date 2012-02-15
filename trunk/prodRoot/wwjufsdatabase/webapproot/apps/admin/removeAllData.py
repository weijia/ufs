from google.appengine.ext import db
import libs.GAE.ufsDbGaeTokenDb
import libs.GAE.ufsDbGaeEntryDbV2
import libs.GAE.ufsDbGaeStorage

q = db.GqlQuery("SELECT * FROM ufsEntry")
results = q.fetch(1000)
for result in results:
  result.delete()
  
  
q = db.GqlQuery("SELECT * FROM ufsToken")
results = q.fetch(1000)
for result in results:
  result.delete()
  
  
  
q = db.GqlQuery("SELECT * FROM ufsStorage")
results = q.fetch(1000)
for result in results:
  result.delete()