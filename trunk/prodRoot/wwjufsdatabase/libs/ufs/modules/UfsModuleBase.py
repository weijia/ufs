
class UfsModuleBase(object):
    def listNamedChildren(self, start, cnt, isTree):
        '''
        Shall return res = {"D:/file/full/path/filename": "filename",... }
        '''
        pass
        
    def isChildContainer(self, child):
        '''
        Return True if a child has children
        '''
        return False



def getUfsCollection(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return UfsModuleBase(itemUrl, req.getObjDbSys(),req.getPrimaryUser())
