import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8806/xmlrpc")
    #targetUrl = proxy.register("D:\\sys\\pidgin\\profile", "http://localhost:8806/xmlrpc")
    targetUrl = proxy.register("D:\\sys\\pidgin\\encZip", "http://localhost:8899/xmlrpc")
    print targetUrl