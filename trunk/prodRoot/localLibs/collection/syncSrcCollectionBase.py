import localLibSys
from localLibs.logSys.logSys import *


class objInColInterface(object):
    def getIdInCol(self):
        pass
    def getTimestamp(self):
        pass

class syncSrcCollectionBase(object):
    #############################################
    # The following methods are for synchronizable collection
    #############################################
    def enumObjs(self, timestamp):
        '''
        Must return an object with interface: objInColInterface which has timestamp, idInCol
        '''
        raise "this function must be implemented"
    
    def exists(self, idInCol):
        raise "this function must be implemented"
    
    
    
    #############################################
    # The following method is just used by sub class to provide a enumerator
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
 
