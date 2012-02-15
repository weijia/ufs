import libSys
vfsRootUuid = 'd06a2e46-4300-40f0-a610-60ff802cc1e4'
import libs.utils.configurationTools as configurationTools
import localLibSys
'''
Every local path will start with file://
such as "file:///D:/tmp/"
Every remote path will start with protocol://user:pass@machinename:port/X:/
windows share folder will be:
smb://user@machinename/X:/
'''
class ufsTreeItemBase:
    def getName(self, p):
        pass
        
    def isContainer(self, p):
        '''
        return os.path.isdir(p)
        '''
        pass

    def child(self, fullPath):
        pass
    def getChildAbsPath(self, p):
        return p

def getItemUrl(ufsUrl):
    moduleName, itemUrl = ufsUrl.split(configurationTools.getFsProtocolSeparator(),2)
    return itemUrl
        
def getUfsTreeItem(ufsUrl, req):
    moduleName, itemUrl = ufsUrl.split(configurationTools.getFsProtocolSeparator(),2)
    try:
        ufsItemModule = __import__(moduleName, globals(),locals(),["getUfsTreeItem"], -1)
    except ImportError:
        ufsItemModule = __import__("localLibs.windows."+moduleName, globals(),locals(),["getUfsTreeItem"], -1)
        #print ufsItemModule.getUfsTreeItem(itemUrl, req).listNamedChildren()
    #import winUfs
    #return winUfs.getUfsTreeItem(itemUrl)
    import sys
    #print >>sys.stderr, "creating item"
    #raise "hello world"
    return ufsItemModule.getUfsTreeItem(itemUrl, req)
