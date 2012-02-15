
import libSys
import os
import libs.utils.misc as misc

class tagSystemInterface:
    def tag(self, url, tagList):
        pass
    def getTags(self, url):
        pass
        
#import shove
#import libs.shove.encryptedShove as shove
#import libs.ufsDb.dictShoveDb as dictShoveDb
import libs.ufsDb.dbSys as dbSys

def trimHeadingTailingSpaces(aList):
    res = []
    for i in aList:
        while i[0] == u' ':
            i = i[1:]
        while i[-1] == u' ':
            i = i[0:-1]
        res.append(i)
    return res
    

gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

misc.ensureDir(gAppPath)
misc.ensureDir(gDbPath)

import libs.shove.encryptedListShove as shoveLike
import localLibSys
import localLibs.localDb.sqliteShoveV2 as shove

class tagSystemShoveDb(tagSystemInterface):
    def __init__(self):
        #self.tagDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'tagDb.sqlite'))
        #self.itemTagDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'itemTagDb.sqlite'))
        self.tagDb = shoveLike.ShoveLike(shove.Shove(os.path.join(gDbPath,'tagDb.sqlite')))
        self.itemTagDb = shoveLike.ShoveLike(shove.Shove(os.path.join(gDbPath,'itemTagDb.sqlite')))
        #self.tagDb = shove.Shove('tagDb')
        #self.itemTagDb = shove.Shove('itemTagDb')
        #self.tagDb = dbSys.getDbForTag('tagDb')
        #self.itemTagDb = dbSys.getDbForTag('itemTagDb')
        #dbSysInst = dbSys.dbSysSmart()
        #self.tagDb = dbSysInst.getDbForTag('tagDb')
        #self.itemTagDb = dbSysInst.getDbForTag('itemTagDb')
        

    def tag(self, url, tagList):
        if not (type(tagList) is list):
            tagList = [tagList]
        tagList = trimHeadingTailingSpaces(tagList)
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
            except KeyError:
                self.tagDb[i] = [url]

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
    def getTagDb(self):
        return self.itemTagDb
        
    def getObjs(self, tag):
        return self.tagDb[tag]
                
    def getAllTags(self):
        for i in self.tagDb.keys():
            yield i
            
    def enumObjsWithTag(self, tag):
        for i in self.tagDb.enumValues(tag):
            yield i
            
    def enumObjsWithTagAndTime(self, tag):
        for i, time in self.tagDb.enumValuesWithTime(tag):
            yield (i, time)
            
    def appendTag(self, url, tagList):
        tagList = trimHeadingTailingSpaces(tagList)
        if not (type(tagList) is list):
            tagList = [tagList]
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

    def removeTag(self, url, tagList):
        tagList = trimHeadingTailingSpaces(tagList)
        if not (type(tagList) is list):
            tagList = [tagList]
        try:
            existing = self.itemTagDb[url]
            for i in tagList:
                try:
                    existing.remove(i)
                except ValueError:
                    pass
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
