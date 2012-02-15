from objSync import updatableItemInterface
import jsTreeDbNamedItemParser
import os
import gaeClient
import urllib
  
class gaeItem(updatableItemInterface):
    def __init__(self, itemId, username, password, tmpPath, parentId):
        self.itemId = itemId
        self.tmpPath = tmpPath
        self.username = username
        self.password = password
        self.children = None
        self.parentId = parentId
        print 'parent of ',self.itemId,' is ',self.parentId
        self.dataId = None
        self.server = '127.0.0.1:9901'
        self.server = 'wwjufsdatabase.appspot.com'
        self.serverUrl = "http://%s"%self.server
        self.gaeClientInst = gaeClient.gaeClient(username, password, self.server)


    ###########################################################
    #Followings are updatableItemInterface functions
    ###########################################################
    def child(self, itemId):
        return gaeItem(itemId, self.username, self.password, self.tmpPath, self.itemId)
      
    def rmChild(self, childId):
        p = os.path.join(self.tmpPath, 'delete.txt')
        self.gaeClientInst.rmItem(childId, p)
    
    def listNamedChildren(self):
        if self.children is None:
            self.children = jsTreeDbNamedItemParser.getItemList(self.itemId, self.tmpPath, self.username, self.password, self.serverUrl)
        #self.children contains like {itemId/fullPath (an identifier unique in the whole system): itemName}
        return self.children
    
    def readData(self):
        if self.isContainer():
            return None
        p = os.path.join(self.tmpPath, 'downloading.txt')
        jsTreeDbNamedItemParser.saveData(self.getDataId(), p, self.username, self.password, self.serverUrl)
        print p
        f = open(p,'r')
        res = f.read()
        print len(res)
        f.close()
        return res
    def saveAs(self, targetPath):
        if self.isContainer():
            return None
        jsTreeDbNamedItemParser.saveData(self.getDataId(), targetPath, self.username, self.password, self.serverUrl)
        print 'returnning',targetPath
        return targetPath
    def getDataId(self):
        if self.dataId is None:
            self.dataId = jsTreeDbNamedItemParser.getStorageId(self.itemId, self.tmpPath,self.username,self.password, self.serverUrl)
            if self.dataId is None:
                #Check if it is a container
                if self.isContainer():
                    return self.itemId
        return self.dataId
        
    def updateData(self, childName, srcItem):
        if self.isContainer():
            self.gaeClientInst.addItemWithData(None, childName, self.parentId, self.itemId, srcItem.getDataId())
        data = srcItem.readData()
        if self.getDataId() is None:
            #The item is a new item, add it
            print 'adding item:',childName
            self.gaeClientInst.addItemWithData(data, childName, self.parentId, self.itemId, srcItem.getDataId())
        else:
            print 'updating item:',childName
            self.gaeClientInst.updateItemWithData(data, self.itemId, srcItem.getDataId())

    def getContainer(self):
        '''
        Get the container of this container
        '''
        '''
        fullP = os.path.join(self.p, enStr(relativeP))
        return directoryContainer(fullP)
        '''
        '''
        n = self.treeDb.getObjIdList(sysChildAttr, self.itemId)
        #print n
        if len(n) > 0:
            return n[0]
        else:
            return None
        '''
    def getContainerItem(self):
        itemId = self.getParentItemId()
        return gaeItem(itemId, self.username, self.password, self.tmpPath, None)
        
    def getParentItemId(self):
        if self.parentId is None:
            dataPath = os.path.join(self.tmpPath, 'parentId.txt')
            print self.serverUrl+'/apps/tree/getItemDataId.py?treeRoot=%s&username=%s&passwd=%s'%(self.itemId,self.username,self.password)
            urllib.urlretrieve(self.serverUrl+'/apps/tree/getItemDataId.py?treeRoot=%s&username=%s&passwd=%s'%(self.itemId,self.username,self.password), dataPath)
            f = open(dataPath)
            a = f.read()
            print a
            #print a.find('None')
            if a.find('None')==0:
                return '3fe6382b-0219-40c7-add3-2f3b60aeb368'
            f.close()
            self.parentId = a.split(' ')[0]
        return self.parentId