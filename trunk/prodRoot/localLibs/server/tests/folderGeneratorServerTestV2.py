import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8808/xmlrpc")
    #argv1 task id, argv2 passwd
    proxy.register("d:/proj", "http://localhost:8898/xmlrpc", "testing")