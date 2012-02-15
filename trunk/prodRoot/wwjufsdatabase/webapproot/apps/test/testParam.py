#import libs.GAE.session
#import libs.http.queryParam
#import libs.platform.services
import libSys
import libs.utils.webUtils as webUtils

print "Content-Type: text/html;charset=utf-8"
print ""


f = webUtils.getUnicodeParam()
#print f['sessionId']
#print f['sessionId'][0]

print f