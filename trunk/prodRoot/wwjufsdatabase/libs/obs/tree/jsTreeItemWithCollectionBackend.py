import libSys
import libs.collection.collectionManager as collectionManager
import libs.tree.treeItemInterface as treeItemInterface
import os
import libs.utils.objTools as objTools

class jsTreeItemWithCollectionBackend(treeItemInterface.jsTreeItemInterface):
    def __init__(self, collectionId, parentId, dbSys):
        self.collectionId = collectionId
        self.dbSys = dbSys
        self.parentId = parentId
        self.collection = collectionManager.getCollection(collectionId, dbSys)
    def getContainerItem(self, parentId):
        return parentId
    def listNamedChildren(self, start = 0, cnt = None, getParent = True):
        res = {}
        #import sys
        #print >>sys.stderr, "----------------", start, cnt, type(start)
        for i in self.collection.getRange(start, cnt):
            if objTools.isUfsUrl(i):
                i = getUrlContent(i)
            if getParent:
                if collectionManager.getCollection(i, self.dbSys).isEmpty():
                    continue

            res[i] = os.path.basename(i)
        return res
    def getChildAbsPath(self, p):
        return p
    def isContainer(self, fullPath):
            return True
            
def main():
    import libs.ufsDb.dbSys as dbSys
    f = jsTreeItemWithCollectionBackend('d:/tmp/', None, dbSys)
    print f.listNamedChildren()
    
if __name__=='__main__':
    main()