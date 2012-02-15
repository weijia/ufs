'''
Created on 2011-9-21

@author: Richard
'''
import collectionDatabaseV2 as collectionDatabase
import wwjufsdatabase.libs.utils.transform as transform
import os
import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *

class folderRecursiveEnumCollection(collectionDatabase.collectionOnMongoDbBase):
    '''
    Contain all items in the folder, including files in sub folders, but do not include any folders 
    '''
    def __init__(self, rootDir, dbInst):
        self.rootDir = transform.transformDirToInternal(rootDir)
        self.objDb = dbInst
        collectionDatabase.collectionOnMongoDbBase.__init__(self, self.getCollectionId(self.rootDir),
                                                            dbInst.getCollectionDb())
    def getCollectionId(self, rootDir):
        return u'folderRecursiveEnum://'+transform.transformDirToInternal(rootDir)
    
    #############################################
    # The following methods are called internally, do not use them outside of this class
    #############################################    
    def getRelaPath(self, fullPath):
        #Here use [1:] to remove the leading '/' in front of the relative path
        return transform.formatRelativePath(fullPath.replace(self.rootDir, '')[1:])
    def addFsObj(self, objUrl):
        objUuid = self.objDb.getFsObj(objUrl)["uuid"]
        self.addObj(objUrl, objUuid)
    def getObjUrl(self, idInCol):
        fullPath = transform.transformDirToInternal(os.path.join(self.rootDir, idInCol))
        objUrl = objectDatabase.fsObjBase(fullPath).getObjUrl()
        return objUrl
    def getFullPath(self, idInCol):
        ncl(self.rootDir)
        return transform.transformDirToInternal(os.path.join(self.rootDir, idInCol))
    #############################################
    # The following methods are called when this collection is source collection
    #############################################
    def exists(self, idInCol):
        '''
        This function is called in sync to check if the object exists
        in sync collection to check if the item still exists 
        '''
        objUrl = self.getObjUrl(idInCol)
        #Update the folder collection if the file not exist in file system
        ncl('checking existence', self.getFullPath(idInCol))
        if not os.path.exists(self.getFullPath(idInCol)):
            self.remove(objUrl)
            return False
        else:
            #File exists
            ncl('obj exists', idInCol)
            objExistsInCol = collectionDatabase.collectionOnMongoDbBase.exists(self, objUrl)
            if not objExistsInCol:
                self.addFsObj(objUrl)
            return True

    
    def enumObjs(self, timestamp = 0):
        for i in collectionDatabase.collectionOnMongoDbBase.enumObjs(self, timestamp):
            objUrl = i.getIdInCol()
            ufsObjInst = objectDatabase.ufsObj(objUrl)
            fullPath = transform.transformDirToInternal(ufsObjInst["fullPath"])
            ncl(fullPath)
            #Update the folder collection if the file not exist in file system
            if not os.path.exists(fullPath):
                self.remove(objUrl)
                cl('item deleted in file system', objUrl)
                continue
            j = collectionDatabase.objItemInCol(self.getRelaPath(fullPath), 
                                            i.getUuid(), i.getTimestamp())
            yield j
            
            
    #############################################
    # The following methods are called when this collection are both src and dest
    # Called by archiver? only?
    #############################################    
    def getObjUuid(self, idInCol):
        ################################
        #The following must call base class's exists, as exists in this class 
        #is overrided
        if os.path.exists(self.getFullPath(idInCol)):
            objUrl = self.getObjUrl(idInCol)
            if not collectionDatabase.collectionOnMongoDbBase.exists(self, objUrl):
                self.addFsObj(objUrl)
            itemUuid = collectionDatabase.collectionOnMongoDbBase.getObjUuid(self, self.getObjUrl(idInCol))
            return itemUuid
        return None