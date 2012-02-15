'''
Created on 2011-9-30

@author: Richard
'''

import localLibSys
import localLibs.collection.collectionDatabaseV2 as collectionDatabase

class objCollection(collectionDatabase.collectionOnMongoDbBase):
    '''
    classdocs
    '''
    def __init__(self, collectionId, objDbInst):
        self.objDb = objDbInst
        collectionDatabase.collectionOnMongoDbBase.__init__(self, collectionId, objDbInst.getCollectionDb())

    def append(self, objUfsUrl, idInCol = None):
        if idInCol is None:
            idInCol = objUfsUrl
        newObj = self.objDb.getFsObjFromUfsUrl(objUfsUrl)
        self.updateObjUuidIfNeeded(idInCol, newObj["uuid"])
