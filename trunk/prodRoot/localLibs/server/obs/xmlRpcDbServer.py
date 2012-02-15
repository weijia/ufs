from cherrypy import _cptools
import cherrypy
import localLibSys
import localDbSys
import wwjufsdatabase.libs.tag.sessionBase as sessionBase
class Root:
    def index(self):
        return "I'm a standard index!"
    index.exposed = True

class dictDbRpcServer(_cptools.XMLRPCController):
    def __init__(self, dbMod = localDbSys):
        self.dbMod = dbMod
        self.dbDict = {}
        self.dbSysDict = {}
        _cptools.XMLRPCController.__init__(self)
        
    def getDb(self, user, dbName):
        try:
            db = self.dbDict[(user, dbName)]
        except KeyError:
            if user is None:
                dbSys = self.dbMod.dbSysSmart()
            else:
                dbSys = self.dbMod.dbSysSmart(sessionBase.sessionInstanceBase(user))
            db = dbSys.getDb(dbName)
            self.dbDict[(user, dbName)] = db
        return db
        
    def getValues(self, user, dbName, key):
        key = unicode(key)
        print key, type(key)
        return self.getDb(user, dbName)[key]
    getValues.exposed = True
    
    def setValues(self, user, dbName, key, value):
        self.getDb(user, dbName)[key] = value
        return value
    setValues.exposed = True
        
    def getKeys(self, user, dbName, start, end, timeStamp):
        return self.getDb(user, dbName).keys()
    getKeys.exposed = True


if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    root = Root()
    root.xmlrpc = dictDbRpcServer()

    cherrypy.config.update({'environment': 'production',
                            'log.error_file': '../../../../site.log',
                            'log.screen': True,
                            'engine.autoreload_on' : True,
                            'server.socket_port' : 8805,
                            'request.dispatch': cherrypy.dispatch.XMLRPCDispatcher(),
                            'tools.xmlrpc.allow_none': 1,})

    cherrypy.quickstart(root, '/')    
