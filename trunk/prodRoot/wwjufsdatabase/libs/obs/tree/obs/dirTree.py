import libSys
from treeItemInterface import readOnlyTreeItemInterface
import os
import shove
from desktopApp.lib.transform import *
import uuid
import libs.utils.misc
import libs.cache.collectionCache
gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

        
libs.utils.misc.ensureDir(gAppPath)
libs.utils.misc.ensureDir(gDbPath)

pathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'pathDb.sqlite'))
uuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'uuidDb.sqlite'))


class dirTree(readOnlyTreeItemInterface):
    def __init__(self, fullPath):
        self.fullPath = transformDirToInternal(fullPath)
        try:
            u = pathDb[fullPath]
        except KeyError:
            u = str(uuid.uuid4())
            pathDb[path] = u
            uuidDb[u] = path
        self.uuid = u

    def listNamedChildrenPerRangeWithAutoRefresh(self, start, cnt):
        i = self.childGenerator()
        return libs.cache.collectionCache(i, self.uuid)
        
    def childGenerator(self):
        for i in os.listdir(self.fullPath):
            yield i.decode("gb2312")