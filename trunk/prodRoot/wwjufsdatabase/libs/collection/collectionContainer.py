import collectionInterface as collectionInterface
import collectionManager

class interfaceFunctionNotSupported: pass


class collectionContainerWrapperForPythonList:
    def __init__(self, pythonList):
        self.pythonList = pythonList
    def getRange(self, start, cnt):
        if cnt is None:
            return self.pythonList[start:]
        return self.pythonList[start:start+cnt]


class collectionContainer(collectionInterface.readOnlyCollectionInterface):
    def __init__(self, rootCollection, dbSysInst):
        self.rootCollection = rootCollection
        self.dbInst = dbSysInst
        self.filterList = []
    def setFilter(self, filterList):
        self.filterList = filterList
        
    def hasElem(self, anElem):
        '''
        Check if element is in the list
        '''
        raise interfaceFunctionNotSupported()
    def getRange(self, start, cnt):
        '''
        Get the elements from start to start+cnt (include start but not start+cnt)
        '''
        co = self.rootCollection.getRange(0, None)
        #Can res = co work? Or res.extend(co)?
        #print co
        res = []
        for i in co:
            if i in self.filterList:
                continue
            res.append(i)
        #Find all element
        for i in co:
            if i in self.filterList:
                continue
            childCo = collectionManager.getCollection(i, self.dbInst)
            childCoContainer = collectionContainer(childCo, self.dbInst)
            partRes = childCoContainer.getRange(0, None)
            res.extend(partRes)
            #print "adding:",partRes,i
            if not (cnt is None):
                if len(res) >= start+cnt:
                    #3 element, start=2 cnt=1, OK
                    #3 element, start=3 cnt=1, not OK
                    break
            
        #Found all required element, return
        #print "start:",start
        #print "cnt:",cnt
        #print len(res)
        if cnt is None:
            return res[start:]
        return res[start:start+cnt]
        
        
def main():
    import localLibs.test.testDbSys as testDbSys
    res = {}
    d = testDbSys.testDbSys()
    co = collectionManager.getCollection('G:/app/wwj/cryptload', d)
    print '\n\n\n'
    h=collectionContainer(co, d).getRange(50, 50)
    print '\n\n\n'
    print h
    
if __name__=='__main__':
    main()