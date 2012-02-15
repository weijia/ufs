import libSys
import libs.utils.configurationTools as configurationTools
import localLibSys
'''
Every local path will start with file://
such as "file:///D:/tmp/"
Every remote path will start with protocol://user:pass@machinename:port/X:/
windows share folder will be:
smb://user@machinename/X:/
'''
vfsRootUuid = 'd06a2e46-4300-40f0-a610-60ff802cc1e4'


def getUfsCollection(ufsUrl, req):
    moduleName, itemUrl = ufsUrl.split(configurationTools.getFsProtocolSeparator(),2)
    try:
        #Equal to from moduleName import getUfsCollection
        #Use moduleName.getUfsCollection to call this function
        ufsItemModule = __import__("modules."+moduleName, globals(),locals(),["getUfsCollection"], -1)
    except ImportError:
        ufsItemModule = __import__("localLibs.windows."+moduleName, globals(),locals(),["getUfsCollection"], -1)
        #print ufsItemModule.getUfsTreeItem(itemUrl, req).listNamedChildren()
    #import winUfs
    #return winUfs.getUfsTreeItem(itemUrl)
    #import sys
    #print >>sys.stderr, "creating item"
    #raise "hello world"
    #print ufsItemModule
    return ufsItemModule.getUfsCollection(itemUrl, req)
