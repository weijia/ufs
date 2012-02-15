'''
$Id
Created on 2011-11-4

@author: Richard
'''

import syncSrcCollectionInterface

class folderWithContainer(syncSrcCollectionInterface.syncSrcCollectionInterface):
    '''
    classdocs
    '''
    def __init__(self, syncSrcStateObjId):
        '''
        Sync state for the destination collection, this method may probably be overrided
        '''
        self.syncSrcStateObjId = syncSrcStateObjId
    def enumObjs(self, srcStateObjId):
        '''
        Enumerate new objects in collection from the last saved state.
        '''
        pass
    def updateState(self, srcStateObjId):
        '''
        When this function was called the item just returned has been processed.
        State of the enumeration should be updated.
        '''
        pass
    def getObjUuid(self, idInCol):
        '''
        Return the object uuid so syncer can check if update needed.
        '''
        pass
    def exists(self, idInCol):
        pass
        
        
class folderWithContainerFactory(syncSrcCollectionInterface.syncSrcCollectionFactoryInterface):
    def getSrcCollection(self, syncSrcStateObjId):
        return folderWithContainer(syncSrcStateObjId)