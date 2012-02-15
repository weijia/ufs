import libs.html.response
import libs.platform.services


h = libs.html.response.html()

q = libs.platform.services.getQueryService()
f = q.getAllFieldStorage()


h.genHead()
print f
h.genForm('/apps/test/uploadFileTest.py',[['f','uploadFile']])
h.genEnd()