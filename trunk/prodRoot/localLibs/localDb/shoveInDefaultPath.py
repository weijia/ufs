import localLibSys
import os
import sqliteListShoveWithHistory
import wwjufsdatabase.libs.utils.misc as misc

gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

misc.ensureDir(gAppPath)
misc.ensureDir(gDbPath)

class ShoveForSession(sqliteListShoveWithHistory.Shove):
    def __init__(self, sqliteDbName, sessionInstance, dbPath = gDbPath):
        if sessionInstance is None:
            path = os.path.join(dbPath,sqliteDbName+".sqlite")
        else:
            p = sessionInstance.getDbPath(dbPath)
            path = os.path.join(p, sqliteDbName+".sqlite")
        sqliteListShoveWithHistory.Shove.__init__(self, path)
        self.sessInst = sessionInstance


class Shove(sqliteListShoveWithHistory.Shove):
    def __init__(self, sqliteDbName, dbPath = gDbPath):
        if sessionInstance is None:
            path = os.path.join(dbPath,sqliteDbName+".sqlite")
        else:
            p = sessionInstance.getDbPath(dbPath)
            path = os.path.join(p, sqliteDbName+".sqlite")
        sqliteListShoveWithHistory.Shove.__init__(self, path)