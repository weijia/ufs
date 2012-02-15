import ufsDbGaeListShoveLike as gaeShoveLike
import libSys
import libs.platform.ufsDbManager as dbMan

class ShoveForSession(gaeShoveLike.shoveLike):
    def __init__(self, dbName, sessionInstance):
        self.sessInst = sessionInstance
        mngr = dbMan.ufsDbManager()
        u = sessionInstance.getUser()
        db = mngr.getSimpleDb(u, dbName)
        gaeShoveLike.shoveLike.__init__(self, db)


class Shove(gaeShoveLike.shoveLike):
    def __init__(self, dbName):
        mngr = usrMan.ufsDbManager()
        u = usrMan.ufsUserExample("test")
        db = mngr.getSimpleDb(u, dbName)
        gaeShoveLike.shoveLike.__init__(self, db)


