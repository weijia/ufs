import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8805/xmlrpc/")

today = proxy.getKeys("hi", "ho", "no", "go")
print today