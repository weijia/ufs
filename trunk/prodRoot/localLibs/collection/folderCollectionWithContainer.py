'''
Created on 2011-9-21

@author: Richard
'''
import collectionDatabaseV3 as collectionDatabase
import wwjufsdatabase.libs.utils.transform as transform
import os
import localLibs.collection.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *

class folderCollectionWithContainer(collectionDatabase.collectionOnMongoDbBase):
    '''
    Contain all items in the folder, not including files in sub folders and
     do not include any folder items, this class will check the existence of
     the database element in the file system but will not add new element to database
    '''
    def __init__(self, rootDir, dbInst):
        self.rootDir = transform.transformDirToInternal(rootDir)
        self.objDb = dbInst
        super(folderCollectionWithContainer, self).__init__(self.getCollectionId(self.rootDir),
                                                            dbInst.getCollectionDb())
    
    def getCollectionId(self, rootDir):
        #return u'folderRecursiveEnum://'+transform.transformDirToInternal(rootDir)
        return self.rootDir


    #############################################
    # The following methods are called when this collection is source collection
    #############################################
    def exists(self, idInCol):
        '''
        This function is called in sync to check if the object exists
        in sync collection to check if the item still exists 
        '''
        fullPath = self.getFullPath(idInCol)
        objUuid = self.getObjUuid(idInCol)
        ufsObjInst = self.getLatestObj(objUuid)
        if ufsObjInst is None:
            return False
        else:
            return True

    def enumObjs(self, timestamp = 0):
        '''
        Enumerate objects in collection, only retrieve data from database. Do not
        scan file system, only the existence is checked.
        If the element in the collection is updated in the file system, the latest item
        will be returned, the uuid in the collection are updated as well.
        '''
        for i in super(folderCollectionWithContainer,self).enumObjs(timestamp):
            #Get full path of the element
            objUuid = i.getUuid()
            ufsObjInst = self.getLatestObj(objUuid)
            #getFsObjFromUuid will return None if the object was deleted, so 
            #check it and handle the case
            if ufsObjInst is None:
                #The object does not exist, remove it from collection
                continue
            #Item exist, return it
            fullPath = transform.transformDirToInternal(ufsObjInst["fullPath"])
            j = collectionDatabase.objItemInCol(self.getRelaPath(fullPath), 
                                            ufsObjInst["uuid"], i["timestamp"])
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
    
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    #############################################
    # The following methods are called internally, do not use them outside of this class
    #############################################
    def getLatestObj(self, objUuid):
        ufsObjInst = self.dbObj.getFsObjFromUuid(objUuid)
        idInCol = ufsObjInst["idInCol"]
        #getFsObjFromUuid will return None if the object was deleted, so 
        #check it and handle the case
        if ufsObjInst is None:
            #The object does not exist, remove it from collection
            self.remove(idInCol)
            return None
        #Item exist, return it
        fullPath = transform.transformDirToInternal(ufsObjInst["fullPath"])
        newUuid = ufsObjInst["uuid"]
        if newUuid != objUuid:
            #Item updated, update it in the collection
            self.updateObjUuid(idInCol, newUuid)
        return ufsObjInst
    
    def getRelaPath(self, fullPath):
        #Here use [1:] to remove the leading '/' in front of the relative path
        relaPath = transform.formatRelativePath(fullPath.replace(self.rootDir, '')[1:])
        if relaPath.find('/') == -1:
            return relaPath
        raise "no recursive folder element in this collection"
    
    def addFsObj(self, objUrl):
        objUuid = self.objDb.getFsObjFromFullPath(objUrl)["uuid"]
        self.addObj(objUrl, objUuid)

    def getFullPath(self, idInCol):
        if (idInCol.find('/') == -1) and (idInCol.find('\\') == -1):
            ncl(self.rootDir)
            return transform.transformDirToInternal(os.path.join(self.rootDir, idInCol))
        else:
            raise "no recursive folder element in this collection"


    
