

class readOnlyCollectionInterface:
    def hasElem(self, anElem):
        '''
        Check if element is in the list
        '''
        pass
    def getRange(self, start, cnt):
        '''
        Get the elements from start to start+cnt (include start but not start+cnt)
        '''
        pass
    def isEmpty(self):
        return False
        
class emptyCollection(readOnlyCollectionInterface):
    def hasElem(self, anElem):
        '''
        Check if element is in the list
        '''
        pass
    def getRange(self, start, cnt):
        '''
        Get the elements from start to start+cnt (include start but not start+cnt)
        '''
        return []
    def isEmpty(self):
        return True

class collectionInterface(readOnlyCollectionInterface):
    def append(self, anElem):
        '''
        Add an item to the end of the list; equivalent to a[len(a):] = [x].
        '''
        pass
    def extend(self, elemList):
        '''
        Extend the list by appending all the items in the given list; equivalent to a[len(a):] = L.
        '''
        pass
        
    def remove(self, anElem):
        '''
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        '''
        pass
