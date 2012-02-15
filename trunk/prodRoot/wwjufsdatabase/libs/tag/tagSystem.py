
import libSys
import os
import libs.utils.misc

class tagSystemInterface:
    def tag(self, url, tagList):
        pass
    def getTags(self, url):
        pass
        
#import shove
import libs.cache.encryptedShove as shove

gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

        
libs.utils.misc.ensureDir(gAppPath)
libs.utils.misc.ensureDir(gDbPath)


class tagSystemShoveDb(tagSystemInterface):
    def __init__(self):
        self.tagDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'tagDb.sqlite'))
        self.itemTagDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'itemTagDb.sqlite'))

    def tag(self, url, tagList):
        if not (type(tagList) is list):
            tagList = [tagList]
        try:
            #print itemTagDb[url]
            #v = itemTagDb[url]
            #v.extend(tagList)
            #itemTagDb[url] = v
            #print v
            #del itemTagDb[url]
            self.itemTagDb[url] = tagList
        except KeyError:
            self.itemTagDb[url] = tagList
        #Update the other db
        for i in tagList:
            try:
                v = self.tagDb[i]
                v.extend(url)
                self.tagDb[i] = v
            except KeyError:
                self.tagDb[i] = [url]

    def getTags(self, url):
        try:
            return self.itemTagDb[url]
        except KeyError:
            return []
            
    def getTagsU(self, url):
        res = []
        l = self.getTags(url)
        for i in l:
            res.append(i.decode('utf8'))
        return res

    def getTagDb(self):
        return self.itemTagDb
        
    def getObjs(self, tag):
        return self.tagDb[tag]
                
        
if __name__ == '__main__':
    t = tagSystemShoveDb()
    t.tag('good', 'bad')
    #print t.getTags('good')
    #print t.getTags('good')
    print t.getTags('D:/sys/pic/DSCF0015.JPG')
    #t.tag('D:/sys/pic/DSCF0015.JPG','tag')
    for i in t.getTags('D:/sys/pic/DSCF0015.JPG'):
        print unicode(i).decode('utf8')
    print t.getObjs('bad')