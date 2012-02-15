'''
Created on 2011-9-28

@author: Richard
'''
import os

import ufsObj
import localLibSys
import collectionDatabaseV2 as collectionDatabase
import objectDatabaseV3 as objectDatabase
import wwjufsdatabase.libs.utils.transform as transform
from localLibs.logSys.logSys import *



class folderCacheOnDb(collectionDatabase.collectionOnMongoDbBase):
    '''
    classdocs
    '''
    def __init__(self, folderPath, objDbInst, collectionId = None):
        '''
        Constructor
        '''
        self.objDbInst = objDbInst
        self.folderPath = transform.transformDirToInternal(folderPath)
        if collectionId is None:
            collectionId = ufsObj.getUfsUrlForPath(folderPath)
        collectionDatabase.collectionOnMongoDbBase.__init__(self, collectionId, objDbInst.getCollectionDb())
            
            
    def refreshCache(self):
        #Check if the objects in collection still exists
        for i in collectionDatabase.collectionOnMongoDbBase.enumObjs(self, 0):
            j = self.objDbInst.getObjFromUuid(i.getUuid())
            if not os.path.exists(j["fullPath"]):
                self.remove(i.getIdInCol())
        
        for i in os.listdir(self.folderPath):
            fullPath = os.path.join(self.folderPath, i)
            if os.path.isdir(fullPath):
                #It is a container, add it to collection
                fsObj = self.objDbInst.getFsContainerObjFromFullPath(fullPath)
            else:
                fsObj = self.objDbInst.getFsObjFromFullPath(fullPath)
            ufsUrl = fsObj.getObjUfsUrl()
            if self.exists(ufsUrl):
                ncl('obj exists', ufsUrl)
                oldUuid = self.getObjUuid(fsObj.getObjUfsUrl())
                if fsObj["uuid"] == oldUuid:
                    ncl('object not updated')
                    continue
            #Item does not exists, or item updated, update it in the collection
            self.updateObjUuid(fsObj.getObjUfsUrl(), fsObj["uuid"])
        
def main():
    objDb = objectDatabase.objectDatabase()
    f = folderCacheOnDb('d:/tmp', objDb)
    f.refreshCache()
    for i in f.enumObjs():
        print i.getIdInCol()
        print objDb.getObjFromUuid(i.getUuid())
    
     
if __name__ == '__main__':
    main()