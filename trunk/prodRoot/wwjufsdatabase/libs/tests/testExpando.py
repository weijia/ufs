from google.appengine.ext import db

class testExpando(db.Expando):
  objId = db.StringProperty(required=True)
  
print "Content-Type: text/html;charset=utf-8"
print ""
  
  
attr = {'hello':'good','bad':'ok'}
t = testExpando(objId ='noobjectid',**attr)
t.put()

print dir(t)
print t.dynamic_properties()
print getattr(t, 'hello')