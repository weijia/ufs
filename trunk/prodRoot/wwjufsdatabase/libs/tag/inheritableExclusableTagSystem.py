import inheritableTagSystem
import libSys
import libs.collection.cachedCollection as cachedCollection
import libs.ufsDb.dbSys as dbSys
import tagSystemV2

class tagSystemNonExcludedTag: pass

class tagSystemShoveDb(inheritableTagSystem.tagSystemShoveDb):
    '''
    tag start with u"," is treated as non-tag.
    '''
    def getExcludedTagPrefix(self):
        return u','
    def getExcludedTag(self, tag):
        if self.isExcludedTag(tag):
            return tag[1:]
        raise tagSystemNonExcludedTag()
    def isExcludedTag(self, tag):
        return (tag[0] == self.getExcludedTagPrefix())
    def getExcludedTagStr(self, tag):
        return self.getExcludedTagPrefix()+tag
    
    def filterExcluded(self, tags):
        filtered = []
        included = []
        excluded = []
        #Find all excluded tags
        for i in tags:
            if i[0] == self.getExcludedTagPrefix():
                excluded.append(i[1:])
            else:
                included.append(i)
        #Find all final tags
        for i in included:
            if i in excluded:
                continue
            filtered.append(i)
        return filtered

    
    def getTags(self, url):
        #Tag for the current element override the inherited tag
        inherit = self.getInheritedTags(url)
        filtered = self.filterExcluded(inherit)
        res = tagSystemV2.tagSystemShoveDb.getTags(self, url)
        res.extend(filtered)
        return list(set(self.filterExcluded(res)))

    def tag(self, url, tagList):
        tagList = self.formatTagList(tagList)
        inheritTags = self.getInheritedTags(url)
        include = []
        for i in inheritTags:
            #Don't apply if parent has the tag? No
            if i in tagList:
                include.append(i)
            else:
                #Exclude this tag
                include.append(self.getExcludedTagPrefix()+i)
        #Add non-inheritTags
        for i in tagList:
            if not (i in include):
                include.append(i)
        inheritableTagSystem.tagSystemShoveDb.tag(self, url, include)
    def removeTag(self, url, tagList):
        tagList = self.formatTagList(tagList)
        inheritedTags = self.getInheritedTags(url)
        excluded = []
        removing = []
        for i in tagList:
            if i in inheritedTags:
                excluded.append(self.getExcludedTagPrefix()+i)
            else:
                removing.append(i)
        #Exclude tags by add "," before tags
        tagSystemV2.tagSystemShoveDb.appendTag(self, url, excluded)
        #Remove tags if it is not inherted
        tagSystemV2.tagSystemShoveDb.removeTag(self, url, removing)
    '''
    def getInheritedTags(self, url):
        inherit = inheritableTagSystem.getInheritedTags(self, url)
        included = []
        excluded = []
        for i in inherit:
            if self.isExcludedTag(i):
                excluded.append(getExcludedTag(i))
            else:
                included.append(i)
        #Remove excluded tags
        res = []
        for i in included:
            if i in excluded:
                continue
            else:
                res.append(i)
        return res
    '''
    '''
    #Use the default tag system appendTag function
    def appendTag(self, url, tagList):
        inheritTags = self.getInheritedTags(url)
        for i in tagList:
            #Check if the tag is excluded, if it is excluded, remove the excluding tag
            if self.getExcludedTagStr(i) in inheritTags:
    '''         
    '''
    def getObjs(self, tag):
        raise "not supported"
    '''
    def getAllTags(self):
        for i, j in inheritableTagSystem.tagSystemShoveDb.getAllTags(self):
            if self.isExcludedTag(i):
                continue
            yield i, j

if __name__ == '__main__':
    t = tagSystemShoveDb()
    print t.getTags(u'D:/Downloads/game/76-in-1 [p1][!].zip')
