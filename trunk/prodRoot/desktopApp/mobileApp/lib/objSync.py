import pprint

class updatableItemInterface:
    def child(self, itemId):
        pass
    def rmChild(self, itemId):
        pass
    def listNamedChildren(self):
        '''
        Must return None if it is not a container
        '''
        pass

    def readData(self, dataId):
        pass
    def getDataId(self):
        pass
    def saveAs(self):
        return None
    def updateData(self, childName, srcChildItem):
        pass
    def isContainer(self):
        if len(self.listNamedChildren()) > 0:
            return True
        else:
            return False

class objUpdater:
    def updateChildren(self, srcItem, dstItem):
        #Get items in srcItem
        srcChildren = srcItem.listNamedChildren()
        #Get items in dstItem
        dstChildren = dstItem.listNamedChildren()
        #print 'dst children:',dstChildren
        #print 'src children:',srcChildren
        #Remove all items that exist in dstItem but not in srcItem
        if dstChildren is None:
            print 'no itme need to be removed'
        else:
            print 'removing old children'
            for i in dstChildren.keys():
                if not srcChildren.has_key(i):
                    #Not in src, remove from current dst list (may be backuped somewhere)
                    print 'item :%s removed'%i
                    dstItem.rmChild(i)
        #Update all items that need to be updated
        print 'update new children'
        for i in srcChildren.keys():
            #pprint.pprint(dstChildren)
            dstChild = dstItem.child(i)
            srcChild = srcItem.child(i)
            #print 'updating child'
            srcDataId = srcChild.getDataId()
            #print 'chekding if update needed:',dstChild.getDataId(), srcDataId
            print '---------------------------checking:', srcChildren[i]
            if (srcDataId != None) and (dstChild.getDataId() != srcDataId):
                print 'update the item:',srcChildren[i]
                #print 'Name: %s, srcDataId: %s, dstChild.getDataId(): %s'%(srcChildren[i], srcDataId, dstChild.getDataId())
                dstChild.updateData(srcChildren[i], srcChild)
            else:
                print 'no update required'
            if srcChild.isContainer():
                #print 'update children'
                self.updateChildren(srcChild, dstChild)
