
import libs.cache.collectionCache


class nullLog:
    def l(self, s):
        pass

def cachedCollectionIterFromRange(collectionId, iter, start, cnt, log = nullLog()):
    ci = libs.cache.collectionCache.collectionCache(collectionId)
    #yield 'before list', 'before list'
    l = ci.listNamedChildrenPerRangeWithAutoRefresh(start, cnt, iter, log)
    return l


def cachedCollectionIter(collectionId, iter, page, log = nullLog()):
    imgPerLine = 1
    imgRowPerPage = 12
    start = page*imgRowPerPage*imgPerLine
    cnt = imgRowPerPage*imgPerLine
    l = cachedCollectionIterFromRange(collectionId, iter, start, cnt, log = nullLog())
    for i in l:
        yield i

