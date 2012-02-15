import tagSystemV2
import libSys
import libs.collection.cachedCollection as cachedCollection

class tagSystemShoveDb(tagSystemV2.tagSystemShoveDb):
    def getTags(self, url):
        res = tagSystemV2.tagSystemShoveDb.getTags(self, url)
        #Find parent tags
        res.extend(self.getInheritedTags(url))
        res = list(set(res))
        return res
    def getInheritedTags(self, url):
        res = []
        while True:
            try:
                #print url
                parent = cachedCollection.getOriginalParent(url, self.getSysDbInst())
                #print parent
                res.extend(tagSystemV2.tagSystemShoveDb.getTags(self, parent))
                if url == parent:
                    break
                url = parent
            except KeyError:
                #The parent db was not created before it is added? Add it?
                break
        return res
        
if __name__ == '__main__':
    t = tagSystemShoveDb()
    print t.getTags(u'H:/6600_mobile_last/backup')
