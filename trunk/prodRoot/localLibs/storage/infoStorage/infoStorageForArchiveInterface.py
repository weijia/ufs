

class infoStorageForArhiveInterface(object):
        
    def addItem(self, itemObj):
        '''
        itemObj should be a dictionary like object, can get from dbInst.getFsObjFromFullPath(item["fullPath"])
        
        Return value: delta size for the added object
        '''
        pass
    
    def addAdditionalInfo(self, infoDict):
        '''
        Expected to store info dictionary to info["collectionContentInfo"]
        
        Return value: No return value required
        '''
        pass
    
    def finalizeOneTrunk(self):
        '''
        It is used to tell the storage to finalize
        a trunk. It is mostly the controller want to limit the size of trunk in the storage.
        '''
        pass