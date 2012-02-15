import libs.html.response
import uuid

h = libs.html.response.html()
#h.genTxtHead()
print "Content-Type: text/plain;charset=utf-8\n\n",
print '{"uuid":"%s"}'%str(uuid.uuid4())