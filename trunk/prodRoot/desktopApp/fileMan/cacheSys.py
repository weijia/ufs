from desktopApp.lib.transform import *
import shove

gDbPath = 'd:/tmp/fileman/'



lengthDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'lengthDb.sqlite'))
treeDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'treeDb.sqlite'))


class cacheSys:
    def addLocalPath(self, fullPath):
        store