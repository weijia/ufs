import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:9907/xmlrpc")
    #argv1 task id, argv2 passwd
    targetUrl = proxy.create("D:\\tmp\\fileman\\folderInfoStorage\\data", "D:\\proj")
    print targetUrl
