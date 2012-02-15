import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8812/xmlrpc")
    #argv1 task id, argv2 passwd
    targetUrl = proxy.stop()
    print targetUrl