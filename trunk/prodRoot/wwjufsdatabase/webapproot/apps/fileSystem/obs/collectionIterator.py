import uuid
import libs.utils.misc
import shove
import libs.cache.collectionCache
import os
from desktopApp.lib.transform import *



collectionExt=['jpg','jpeg','flv','avi','mp4','rm','rmvb']
gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')


libs.utils.misc.ensureDir(gDbPath)
collectionPreviewPathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewPathDb.sqlite'))
collectionPreviewUuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewUuidDb.sqlite'))


def picIter(fullPath):
    #yield fullPath
    for i in os.listdir(fullPath):
        #yield i
        if libs.utils.misc.withExt(os.path.join(fullPath, i), collectionExt):
            try:
                yield i.decode("gb2312")
            except UnicodeDecodeError:
                continue

        
class nullLog:
    def l(self, s):
        pass

def cachedPicIter(fullPath, page, log = nullLog()):
    imgPerLine = 1
    imgRowPerPage = 8
    fullPath = transformDirToInternal(fullPath)
    try:
        u = collectionPreviewPathDb[fullPath]
    except KeyError:
        u = str(uuid.uuid4())
        collectionPreviewPathDb[fullPath] = u
        collectionPreviewUuidDb[u] = fullPath
    start = page*imgRowPerPage*imgPerLine
    cnt = imgRowPerPage*imgPerLine
    iter = picIter(fullPath)
    ci = libs.cache.collectionCache.collectionCache(u)
    #yield 'before list', 'before list'
    l = ci.listNamedChildrenPerRangeWithAutoRefresh(start, cnt, iter, log)
    #yield 'after list', 'after list'
    if l is None:
        #yield str(start),str(start)
        #yield str(cnt),str(cnt)
        return
    for i in l:
        p = os.path.join(fullPath, i).encode('utf8')
        yield [p,p]
