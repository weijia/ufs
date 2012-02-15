import localLibs.collection.collectionDatabaseV2 as collectionDatabase
import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *

class synchronizableCollection(object):
    #############################################
    # The following methods are for syncronizable collection
    #############################################
    def enumWithPending(self, timestamp, pendingCollection):
        '''
        Enumerate collection items, items are return, not objects
        '''
        ####################
        #First, process items in pending list
        ####################
        #Get item from source collection and check if it is still in the original list
        for processingObjInCol in pendingCollection.enumObjs(0):
            cl("enum pending", processingObjInCol.getIdInCol())
            if not self.exists(processingObjInCol.getIdInCol()):
                #Dosen't exist anymore, ignore it
                cl('Does not exist any more')
                del pendingCollection[processingObjInCol.getIdInCol()]
                continue
            ###########################
            # Returning collection item and timestamp
            ###########################
            yield processingObjInCol, timestamp
            
        ####################
        #Process items after the timestamp
        ####################
        ncl("timestamp:", timestamp)
        for processingObjInCol in self.enumObjs(timestamp):
            cl("enum collection", processingObjInCol.getIdInCol())
            #Check if the log file and data file are both OK
            yield processingObjInCol, processingObjInCol.getTimestamp()
    
    '''
    def complete(self, obj, pendingCollection):
        if pendingCollection.exists(obj.getIdInCol()):
            del pendingCollection[obj.getIdInCol()]
    '''     
    def exists(self, idInCol):
        '''
        Check if the item is still in this collection, called in self.enumWithPending
        '''
        raise "not implemented"
    
        
    def store(self, obj):
        raise "not implemented"
    
    '''
    def enumObjWithPendingCollection(self, timestamp, pendingCollection):
        pass
    '''