import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8806/")

# Print list of available methods
print proxy.system.listMethods()