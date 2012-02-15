from collectionInterface import collectionInterface

class collectionBase(collectionInterface):
    def __init__(self, collectionId, shoveListDb):
        self.shoveListDb = shoveListDb
        self.collectionId = collectionId
        self.timeStamp = None
    def append(self, anElem):
        '''
        Add an item to the end of the list; equivalent to a[len(a):] = [x].
        '''
        self.shoveListDb.append(self.collectionId, anElem)
    def extend(self, elemList):
        '''
        Extend the list by appending all the items in the given list; equivalent to a[len(a):] = L.
        '''
        self.shoveListDb.append(self.collectionId, elemList)
        
    def remove(self, anElem):
        '''
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        '''
        self.shoveListDb.remove(self.collectionId, anElem)
    def hasElem(self, anElem):
        '''
        Check if element is in the list
        '''
        return self.shoveListDb.hasValue(self.collectionId, anElem)
    def getRange(self, start, cnt):
        '''
        Get the elements from start to start+cnt (include start but not start+cnt)
        '''
        if self.timeStamp is None:
            self.timeStamp = self.shoveListDb.getSnapshotTimestamp()
        if cnt is None:
            cnt = None
        res = self.shoveListDb.getSnapshotValueRange(self.collectionId, self.timeStamp, start, cnt)
        #res.append(self.collectionId)
        return res
    def refresh(self):
        self.timeStamp = self.shoveListDb.getSnapshotTimestamp()
    def update(self, elemList):
        del self.shoveListDb[self.collectionId]
        self.extend(elemList)