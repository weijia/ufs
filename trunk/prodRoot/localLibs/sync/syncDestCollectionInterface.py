'''
Created on 2011-11-1

@author: Richard
'''

class syncDestCollectionInterface(object):
    '''
    classdocs
    '''
    def __init__(self, syncDestStateObjId):
        '''
        Sync state for the destination collection, this method may probably be overrided
        '''
        self.syncDestStateObjId = syncDestStateObjId

    def store(self, storingObj):
        '''
        Store storingObj to this collection. If the processing is not completed, add it to pendingCollection
        '''
        pass
    
    def exists(self, idInCol):
        '''
        Check if the idInCol exist in this collection, if exist, the getObjUuid of this class will be
        called and the item with idInCol will be used to compare with the source object from source
        collection
        '''
        pass
    
    def getObjUuid(self, idInCol):
        '''
        Will be called if idInCol exists
        '''
        pass
    
    def enumEnd(self):
        '''
        Called through destination when enumeration of source collection ended.
        '''
        pass
    
class syncDestCollectionFactoryInterface(object):
    def getDestCollection(self, syncDestStateObjId):
        return syncDestCollectionInterface(syncDestStateObjId)