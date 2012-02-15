import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8902/xmlrpc")
    #argv1 task id, argv2 passwd
    targetUrl = proxy.create("d:/tmp", 10)
    print targetUrl
