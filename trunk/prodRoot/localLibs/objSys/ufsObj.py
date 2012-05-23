'''
Created on 2011-9-28

@author: Richard
'''
import UserDict
import os
import copy

import localLibSys
import localLibs.localTasks.infoCollector as infoCollector
import wwjufsdatabase.libs.utils.transform as transform
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.objTools as objTools
from localLibs.utils.misc import get_prot_root
import magic

def get_mime_type(file_full_path):
    rootPath = get_prot_root()
    magicPath = os.path.join(rootPath, "share\\file\\magic")
    #print 'magic path: ',magicPath
    if not os.path.exists(magicPath):
        raise "Magic file lost"
    #print "magic path is", magicPath
    #os.environ["MAGIC"] = magicPath
    m = magic.Magic(magic_file=magicPath)
    res = m.from_file(file_full_path)
    return res

class objBase(UserDict.DictMixin):
    def __init__(self, existingItemInfo = {}):
        self.itemInfo = copy.copy(existingItemInfo)
        if self.itemInfo.has_key("_id"):
            del self.itemInfo["_id"]
        
    def __getitem__(self, key):
        if self.itemInfo.has_key(key):
            return self.itemInfo[key]
        funcAttr = getattr(self, key)
        value = funcAttr()
        self.itemInfo[key] = value
        return value
    def has_key(self, key):
        try:
            self.__getitem__(key)
            return True
        except AttributeError:
            return False

    def __setitem__(self, key, value):
        self.itemInfo[key] = value
        return value

    def __delitem__(self, key):
        del self.itemInfo[key]
    
    def keys(self):
        return self.itemInfo.keys()
        
    def get_full_path(self):
        #self.fillInfo("fullPath")
        return self.itemInfo["fullPath"]
    
    def get_uuid(self):
        return self.itemInfo["uuid"]

    def getItemInfo(self):
        return self.itemInfo
    

class fsObjBase(objBase):
    def __init__(self, fullPath, existingItemInfo = {}):
        self.fullPath = transform.transformDirToInternal(fullPath)
        self.itemInfo = copy.copy(existingItemInfo)
        self.itemInfo["fullPath"] = self.fullPath
        if self.itemInfo.has_key("_id"):
            del self.itemInfo["_id"]
    def isContainer(self):
        return os.path.isdir(self.fullPath)
    
    def exists(self):
        return os.path.exists(self.fullPath)
    #########################################################
    #The following methods are for dict
    #########################################################
    def itemAttr(self, key):
        if self.itemInfo.has_key(key):
            #print 'has key:', key
            return self.itemInfo[key]
        else:
            #print 'calling func:', key
            self.itemInfo[key] = getattr(self, key)()
            return self.itemInfo[key]
        
    def fillInfo(self, attrName):
        res = {}
        for i in attrName:
            res[i] = self.itemAttr(i)
        return res
        
    def size(self):
        #print '%s size: %d'%(self.fullPath, os.stat(self.fullPath).st_size)
        return os.stat(self.fullPath).st_size
    
    def timestamp(self):
        return os.stat(self.fullPath).st_mtime
    
    def headMd5(self):
        #raise "generating md5"
        ncl("Generating Md5")
        try:
            return infoCollector.getHeadContentMd5(self.fullPath)
        except IOError:
            return None
    def mime_type(self):
        return get_mime_type(self.fullPath)
        
    def getItemInfo(self):
        tmp = self.fillInfo(["timestamp", "fullPath"])
        return self.itemInfo
    
    def getItemObjUrl(self):
        return self.getObjUrl()
    
    def getObjUrl(self):
        return u"file:///"+self.fullPath
    
    def getObjUfsUrl(self):
        return objTools.getUfsUrlForPath(self.fullPath)

class detailedFsObj(fsObjBase):
    def ufsUrl(self):
        return self.getObjUfsUrl()
    def getItemInfo(self):
        tmp = self.fillInfo(["timestamp", "fullPath", "headMd5", "size", "ufsUrl", "uuid"])
        return self.itemInfo

class fsDirObj(fsObjBase): pass

class fsObj(fsObjBase):
    def getItemInfo(self):
        tmp = self.fillInfo(["timestamp", "fullPath", "headMd5", "size"])
        return self.itemInfo
    
class ufsUrlObj(fsObj):
    '''
    Object initialized using file:///C:/xxx/xxx format
    '''
    def __init__(self, objUrl, existingItemInfo = {}):
        self.objUrl = objUrl
        objPath = objTools.getFullPathFromUfsUrl(objUrl)
        ncl('ufsUrlObj fullPath:', objPath)
        fsObj.__init__(self, objPath, existingItemInfo)
         
class ufsObj(fsObj):
    def __init__(self, objUrl, existingItemInfo = {}):
        self.objUrl = objUrl
        objPath = objTools.parseUrl(objUrl)[1][1:]
        ncl('ufsObj fullPath:', objPath)
        fsObj.__init__(self, objPath, existingItemInfo)
        
class objInCollection(fsObjBase):
    def __init__(self, idInCol, itemInfo):
        objBase.__init__(self, itemInfo)
        self.itemInfo["idInCol"] = transform.formatRelativePath(idInCol)
        
    def getIdInCol(self):
        return self.itemInfo["idInCol"]