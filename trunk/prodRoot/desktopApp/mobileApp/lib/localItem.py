from objSync import updatableItemInterface
import timestamp
import shutil
import os
import pprint
import md5
from stat import *
import uuid


def initDict(d, childDictName):
    if not d.has_key(childDictName):
        #pprint.pprint(d)
        #print 'creating:',childDictName
        d[childDictName] = {}
  
class localJsonItem(updatableItemInterface):
    def __init__(self, itemId, parentPath, jsonDb, backupPath):
        #print '--------------------------------------------'
        #pprint.pprint(jsonDb)
        self.parentPath = parentPath
        if not os.path.exists(self.parentPath):
            os.mkdir(self.parentPath)
        self.itemId = itemId
        self.itemName = None
        self.backupPath = backupPath
        self.jsonDb = jsonDb
        self.children = None
        #pprint.pprint(self.jsonDb)
        initDict(self.jsonDb, 'children')
        initDict(self.jsonDb, 'name')
        initDict(self.jsonDb, 'deletedChild')
        initDict(self.jsonDb, 'dataId')
        #initDict(self.jsonDb, 'md5')
        #initDict(self.jsonDb, 'size')
        initDict(self.jsonDb, 'lastModified')


    def getItemName(self):
        if self.itemName is None:
            self.itemName = self.jsonDb['name'].get(self.itemId, self.itemId)
        #print self.jsonDb['name']
        #if self.itemName is None:
        #    print self.jsonDb['name'], self.itemId
        return self.itemName
    def getPath(self):
        if self.getItemName() is None:
            raise 'no name defined'
        #print self.parentPath, self.getItemName()
        curItemPath = os.path.join(self.parentPath, self.getItemName())
        #print curItemPath
        #if not os.path.exists(curItemPath):
        #    print 'creating ',curItemPath
        #    os.mkdir(curItemPath)
        return curItemPath
    def isUpdated(self):
        if self.exists():
            if self.jsonDb['lastModified'].get(self.itemId, None) == os.stat(self.getPath())[ST_MTIME]:
                return False
            print 'update time is:',self.jsonDb['lastModified'].get(self.itemId, None), os.stat(self.getPath())[ST_MTIME]
        return True
        
    def updateDbForLocalCopy(self):
        if self.exists():
            #print 'Path: %s, got from os: %d, get from Db: %d'%(self.getPath(), os.stat(self.getPath())[ST_MTIME], self.jsonDb['lastModified'][self.itemId])
            self.jsonDb['lastModified'][self.itemId] = os.stat(self.getPath())[ST_MTIME]
            #self.jsonDb['md5'][self.itemId] = str(md5.new(data).digest())
            #self.jsonDb['size'][self.itemId] = len(data)
            
    def exists(self):
        if self.getItemName() is None:
            return False
        if self.getPath() is None:
            return False
        if not os.path.exists(self.getPath()):
            return False
        return True
    ###########################################################
    #Followings are updatableItemInterface functions
    ###########################################################
    def child(self, itemId):
        if not self.exists():
            os.mkdir(self.getPath())
        if not self.jsonDb['children'].has_key(self.itemId):
            self.jsonDb['children'][self.itemId] = []
        try:
            self.jsonDb['children'][self.itemId].index(itemId)
        except:
            self.jsonDb['children'][self.itemId].append(itemId)
        return localJsonItem(itemId, self.getPath(), self.jsonDb, self.backupPath)

    def rmChild(self, itemId):
        backupFullPath = os.path.join(self.backupPath, self.getItemName()+timestamp.timestamp())
        try:
            print 'removing: ',self.getPath()
            shutil.move(self.getPath(), backupFullPath)
        except IOError, WindowsError:
            print 'move error'
        if self.jsonDb['children'].has_key(self.itemId):
            self.jsonDb['children'][self.itemId].remove(itemId)
            if not self.jsonDb['deletedChild'].has_key(self.itemId):
                self.jsonDb['deletedChild'][self.itemId] = []
            self.jsonDb['deletedChild'][self.itemId].append(itemId)
            
    def listNamedChildren(self):
        if not self.exists():
            return None
        #print 'all children:',self.jsonDb['children']
        #Add items in local db
        c = self.jsonDb['children'].get(self.itemId, [])
        #print 'childrens:',c
        names = {}
        res = {}
        #Get all names from id list
        for i in c:
            #pprint.pprint(self.jsonDb['name'])
            names[i] = self.jsonDb['name'].get(i, i)
        #print 'child names:',names
        #Add items in local file system
        for i in os.listdir(self.getPath()):
            #print 'checking:',unicode(i)
            #Get id from name in names
            idForName = None
            for k in names.keys():
                #print 'currrent checking:',k
                if names[k] == unicode(i):
                    idForName = k
                    #print 'find name:%s, %s'%(k, idForName)
                    break
            #If the item was not there create an item
            if idForName is None:
                idForName = str(uuid.uuid4())
                self.jsonDb['name'][idForName] = unicode(i)
                #Update the children dict using the following function
                self.child(idForName).updateDbForLocalCopy()
                res[idForName] = unicode(i)
            #Checking for update will be done when getting data id for the item
            res[idForName] = i
        #No other things need to be done. If the item is in children list but not in the dir, it was deleted.
        #print 'returnning:',res
        #Remove children if not exists
        for i in c:
            if not res.has_key(i):
                if not self.jsonDb['deletedChild'].has_key(self.itemId):
                    self.jsonDb['deletedChild'][self.itemId] = []
                self.jsonDb['deletedChild'][self.itemId].append(i)
                try:
                    self.jsonDb['deletedChild'][self.itemId].remove(i)
                except:
                    pass
        #print 'all children:',self.jsonDb['children']
        return res
        
    def readData(self):
        if self.isContainer():
            return None  
        f = open(self.getPath(),'r')
        d = f.read()
        f.close()
        return d
      
    def getDataId(self):
        if self.isContainer():
            return self.itemId
        #print self.jsonDb['dataId'], self.itemId
        if (not self.isUpdated()) and self.jsonDb['dataId'].has_key(self.itemId):
            #dataId exists and it is not updated
            print 'item not updated, return the same data id'
            return self.jsonDb['dataId'][self.itemId]

        print 'id in db:',self.jsonDb['dataId'].has_key(self.itemId)
        print 'data updated, generated a new data id'
        #Generate a new dataId and update local database
        n = str(uuid.uuid4())
        self.jsonDb['dataId'][self.itemId] = n
        self.updateDbForLocalCopy()
        return n

    def updateData(self, childName, srcItem):
        self.jsonDb['name'][self.itemId] = childName
        self.itemName = childName
        print 'creating child:%s'%childName
        if not srcItem.isContainer():
            if srcItem.saveAs(self.getPath()) is None:
                print 'no saveAs, readData()'
                data = srcItem.readData()
                if not (data is None):
                    #The dataId may be an fake id for container
                    f = open(self.getPath(), 'w')
                    f.write(data)
                    f.close()
        self.jsonDb['dataId'][self.itemId] = srcItem.getDataId()
        self.updateDbForLocalCopy()
        
    def isContainer(self):
        if self.exists():
            return os.path.isdir(self.getPath())
        return False