import libSys
import os
#import libs.utils.misc
from localLibs.logSys.logSys import *


class tagSystemInterface:
    def tag(self, url, tagList):
        pass
    def getTags(self, url):
        pass
        
#import shove
#import libs.cache.encryptedShove as shove
#import libs.ufsDb.dictShoveDb as dictShoveDb

def trimHeadingTailingSpaces(aList):
    res = []
    for i in aList:
        while i[0] == u' ':
            i = i[1:]
        while i[-1] == u' ':
            i = i[0:-1]
        res.append(i)
    return res

import sessionBase as sessionBase
    
    
class tagSystemShoveDb(tagSystemInterface):
    def __init__(self, dbSysInst, dbSupportsCnt = False):
        #self.tagDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'tagDb.sqlite'))
        #self.itemTagDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'itemTagDb.sqlite'))
        #self.tagDb = dbSys.getDbForTag('tagDb')
        #self.itemTagDb = dbSys.getDbForTag('itemTagDb')
        self.dbSysInst = dbSysInst
        self.tagDb = dbSysInst.getDbForTag('tagDb')
        self.itemTagDb = dbSysInst.getDbForTag('itemTagDb')
        self.tagStatDb = dbSysInst.getDbForTag('tagStatDb')
        self.dbSupportsCnt = dbSupportsCnt
        
    def getSysDbInst(self):
        return self.dbSysInst
    def formatTagList(self, tagList):
        if not (type(tagList) is list):
            tagList = [tagList]
        return trimHeadingTailingSpaces(tagList)
        
    def tag(self, url, tagList):
        tagList = self.formatTagList(tagList)
        already_in_db = False
        try:
            #The existing values will be deleted by database automatically, so the following is not needed
            #del itemTagDb[url]
            self.itemTagDb[url] = tagList
        except KeyError:
            self.itemTagDb[url] = tagList
        #Update the other db
        #TODO, the removed items are not updated
        for i in tagList:
            try:
                v = self.tagDb[i]
                if not (url in v):
                    v.append(url)
                    self.tagDb[i] = v
                else:
                    # Already in tagDb, ignore this operation
                    already_in_db = True
            except KeyError:
                self.tagDb[i] = [url]
            if not already_in_db:
                try:
                    cnt = int(self.tagStatDb[i][0])
                except KeyError:
                    cnt = 0
                self.tagStatDb[i] = unicode(str(cnt+1))
                print 'add stat for tag:',i , unicode(str(cnt+1))
            
    def getTags(self, url):
        try:
            tags = self.itemTagDb[url]
            if type(tags) == unicode:
                return [tags]
            return tags
        except KeyError:
            return []
    '''        
    def getTagsU(self, url):
        res = []
        l = self.getTags(url)
        for i in l:
            res.append(i.decode('utf8'))
        return res
    '''
    '''
    def getTagDb(self):
        return self.itemTagDb
    ''' 
    def getObjs(self, tag):
        try:
            return self.tagDb[tag]
        except KeyError:
            return []
                
    def getAllTags(self):
        #cl(self.tagDb.__class__)
        if self.dbSupportsCnt:
            print 'using database count'
            for i, j in self.tagDb.keysWithUsage():
                yield i, j
        else:
            #import operator
            tmp = self.tagStatDb.keys()
            dictList = []
            for i in tmp:
                dictList.append((i, self.tagStatDb[i][0]))
            #for i in dictList:
                #print i
                #print int(i[1])
            dictList.sort(key=lambda x:int(x[1]), reverse=True)
            #print '----------------------------------------',dictList
            for i in dictList:
                yield i[0], i[1]
            
    def enumObjsWithTag(self, tag):
        for i in self.tagDb.enumValues(tag):
            #print i
            yield i
    def getAllObjects(self, tag):
        return self.tagDb[tag]

    def enumObjsWithTagAndTime(self, tag):
        for i, time in self.tagDb.enumValuesWithTime(tag):
            yield (i, time)
            
    def appendTag(self, url, tagList):
        tagList = self.formatTagList(tagList)

        try:
            #print itemTagDb[url]
            v = self.itemTagDb[url]
            v.extend(tagList)
            #The existing values will be deleted by database automatically, so the following is not needed
            #del itemTagDb[url]
            self.itemTagDb[url] = v
        except KeyError:
            self.itemTagDb[url] = tagList
        #Update the other db
        #TODO, the removed items are not updated
        for i in tagList:
            try:
                v = self.tagDb[i]
                if not (url in v):
                    v.append(url)
                    self.tagDb[i] = v
            except KeyError:
                self.tagDb[i] = [url]
            try:
                cnt = int(self.tagStatDb[i][0])
            except KeyError:
                cnt = 0
            self.tagStatDb[i] = unicode(str(cnt+1))
            #print 'add stat for tag:',i , unicode(str(cnt+1))

    def removeTag(self, url, tagList):
        tagList = self.formatTagList(tagList)
        try:
            existing = self.itemTagDb[url]
            for i in tagList:
                try:
                    existing.remove(i)
                except ValueError:
                    pass
                #Need to remove it in the tag db
                url_list = self.tagDb[i]
                try:
                    url_list.remove(url)
                    self.tagDb[i] = url_list
                except ValueError:
                    pass
                try:
                    cnt = int(self.tagStatDb[i][0])
                except KeyError:
                    cnt = 0
                if cnt > 1:
                    self.tagStatDb[i] = unicode(str(cnt-1))
                else:
                    del self.tagStatDb[i]
            self.itemTagDb[url] = existing

        except KeyError:
            pass
        #TODO, the removed items are not updated for self.tagDb
                
if __name__ == '__main__':
    t = tagSystemShoveDb()
    '''
    t.tag('good', 'bad')
    #print t.getTags('good')
    #print t.getTags('good')
    print t.getTags('D:/sys/pic/DSCF0015.JPG')
    #t.tag('D:/sys/pic/DSCF0015.JPG','tag')
    for i in t.getTags('D:/sys/pic/DSCF0015.JPG'):
        print unicode(i).decode('utf8')
    print t.getObjs('bad')
    '''
    '''
    for i in t.tagDb.keys():
        print 'find tag:',i
    '''
    '''
    cache = {}
    for file in t.itemTagDb.keys():
        print 'retrieving tag for:%s'%file
        tags = t.itemTagDb[file]
        print 'tag for %s is %s'%(file, str(tags))
        for aTag in tags:
            print 'adding:', aTag,':',file
            if cache.has_key(aTag):
                cache[aTag].append(file)
            else:
                cache[aTag] = [file]
    for i in cache.keys():
        print 'writing files for tag:',cache[i], ',',i
        t.tagDb[i] = cache[i]
    '''
    for i in t.getAllTags():
        print 'retrieving files for tag:', i
        '''
        for j in t.tagDb.getAllRecords():
            print j
        '''
        for j in t.enumObjsWithTagAndTime(i):
            print j
