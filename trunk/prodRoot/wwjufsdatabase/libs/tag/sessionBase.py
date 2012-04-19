import os
import libSys
import localLibSys
import localLibs.utils.misc as misc

class sessionInstanceBase:
    def __init__(self, username):
        self.username = username
    def getDbPath(self, dbPath):
        p = os.path.join(os.path.join(dbPath, 'user'), self.username)
        misc.ensureDir(p)
        return p
    def getUserName(self):
        return self.username