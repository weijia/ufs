#import libSys

import os
#import libs.collection.collectionManager as collectionManager
#import libs.ufsDb.dbSys as dbSys
#import libs.services.nameServiceV2 as nameService
#import libs.utils.configurationTools as configurationTools
#import libs.utils.objTools as objTools
import libs.utils.transform as transform
#import libs.utils.odict as odict
from localLibs.logSys.logSys import *

MAX_ELEMENTS_IN_COLLECTION = 99999

class fileCollection:
    def __init__(self, fullPath, objDbSys, userSession = None):
        #Remove the first / after file:// in file:///D:/
        self.fullPath = transform.transformDirToInternal(fullPath[1:])
        self.objDbSys = objDbSys
        self.userSession = userSession
        #print 'creating file collection', self.fullPath
    def listNamedChildren(self, start, cnt, isTree):
        '''
        Will return res = {"D:/file/full/path/filename": "filename",... }
        '''
        if cnt is None:
            cnt = MAX_ELEMENTS_IN_COLLECTION
        #Retrieve children from database
        folderObj = self.objDbSys.getFsObjFromFullPath(self.fullPath)
        #print folderObj
        if folderObj.has_key("folderCollectionId"):
            folderCol = self.objDbSys.getCollection(folderObj["folderCollectionId"])
            resList = []
            #print 'get collection from db----------------------------------'
            addedCnt = 0
            for i in folderCol.enumObjs():
                resList.append(i.getIdInCol())
                addedCnt += 1
                if addedCnt >= (start+cnt):
                    break
        else:
            #Retrieve children from local service
            import xmlrpclib
            proxy = xmlrpclib.ServerProxy("http://127.0.0.1:9906/xmlrpc")
            if cnt is None:
                cnt = MAX_ELEMENTS_IN_COLLECTION
            resList = proxy.create(self.fullPath, start + cnt, self.userSession.getUserName(), 
                                   self.userSession.getPasswd())
            cl('get collection from service', resList)
        res = {}
        #print start, cnt
        for i in resList[start:(start+cnt)]:
            res[transform.transformDirToInternal(os.path.join(self.fullPath, i))] = unicode(os.path.basename(i))
        return res
        
        
        
    def isChildContainer(self, child):
        '''
        Return True if a child has children
        '''
        for i in self.listNamedChildren(0, 1, False):
            return True
        return False



def getUfsCollection(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return fileCollection(itemUrl, req.getObjDbSys(),req.getPrimaryUser())
