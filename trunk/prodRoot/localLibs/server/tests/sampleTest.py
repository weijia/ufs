import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8901/xmlrpc")
    #argv1 task id, argv2 passwd
    targetUrl = proxy.sampleCreateOnServer()
    print targetUrl
    print "calling thread method"
    print proxy.sampleMethod(targetUrl)
