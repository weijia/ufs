import localLibSys
import wwjufsdatabase.libs.collection.collectionInterface as collectionInterface
import os
from stat import *
import wwjufsdatabase.libs.utils.transform as transform
import sys

class pathNotExist: pass
class pathIsNotCollection: pass

class fileSystemCollection(collectionInterface.readOnlyCollectionInterface):
    def __init__(self, fullPath, folderOnly = False):
        if not os.path.isdir(fullPath):
            raise pathIsNotCollection()
        if not os.path.exists(fullPath):
            raise pathNotExist()
        self.fullPath = transform.transformDirToInternal(fullPath)
        #print self.fullPath
        self.folderOnly = folderOnly
    def hasElem(self, anElem):
        '''
        Check if element is in the list
        '''
        return os.path.exists(anElem)
    def getRange(self, start, cnt):
        '''
        Check if element is in the list
        '''
        res = []
        #print self.fullPath
        #If the param is unicode, it will return unicode
        try:
            d = os.listdir(self.fullPath)
        except WindowsError:
            return []
        #print d
        for i in d:
            if self.folderOnly:
                if not os.path.isdir(os.path.join(self.fullPath,i)):
                    continue
            '''
            if type(i.decode('gbk')) != unicode:
                raise "unknown issue"
            i.decode('utf8').encode('gbk')
            '''
            p = transform.transformDirToInternal(os.path.join(self.fullPath,i))
            #p.encode('utf8')#Test if utf can support decoding filesystem chars.
            res.append(p)
        if cnt is None:
            return res
        return res[start:start+cnt]

    def getCollectionUniversalId(self):
        '''
        Return an ID of the collection, so it can be identified by the cache system and the same object will not be cached twice.
        '''
        if self.folderOnly:
            return u"folder:"+unicode(self.fullPath)
        return unicode(self.fullPath)
    def getRangeWithTimestamp(self, start, cnt, timestamp):
        '''
        Return a list with timestamp
        '''
        #Currently no timestamp checking as the filesystem will not change much during a short period of time
        return self.getRange(start, cnt)
    def lastUpdated(self):
        '''
        Return a timestamp of the last update time
        '''
        return unicode(os.stat(self.fullPath)[ST_MTIME])

def main():
    f = fileSystemCollection('d:/tmp/')
    print f.getRange(0,None)
    f = fileSystemCollection('C:/', True)
    print f.getRange(0,None)
    
if __name__=='__main__':
    main()