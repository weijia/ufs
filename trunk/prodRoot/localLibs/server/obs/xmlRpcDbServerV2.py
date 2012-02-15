from SimpleXMLRPCServer import SimpleXMLRPCServer
#from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import localLibSys
import localDbSys
import wwjufsdatabase.libs.tag.sessionBase as sessionBase
import libs.utils.encodingTools as encodingTools

'''
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
'''
# Create server
server = SimpleXMLRPCServer(("localhost", 8806),allow_none = 1
                            #requestHandler=RequestHandler
                            )
server.register_introspection_functions()
'''
# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)

# Register a function under a different name
def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')
'''
# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
class dictDbRpcServer:
    def __init__(self, dbMod = localDbSys):
        self.dbMod = dbMod
        self.dbDict = {}
        self.dbSysDict = {}
        self.cache = {}
        
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
        #print type(key)
        key = encodingTools.decodeToUnicode(key)
        #print key, type(key)
        #print 'getValue:',user, dbName, key
        try:
            return self.cache[(user, dbName,key)]
        except KeyError:
            pass
        try:
            res = self.getDb(user, dbName)[key]
            self.cache[(user, dbName,key)] = res
            #print 'return get:', user, dbName, key, res
            return res
        except KeyError:
            #print 'no item, return None so client will raise exception'
            return None
    
    def setValues(self, user, dbName, key, value):
        key = encodingTools.decodeToUnicode(key)
        #print 'setting:',value,type(value)
        if not (type(value) == list):
            value = [value]
        uniValue = []
        for i in value:
            uniValue.append(encodingTools.decodeToUnicode(i))
        self.getDb(user, dbName)[key] = uniValue
        self.cache[(user, dbName,key)] = uniValue
        #print 'setting:', user, dbName, key, uniValue
        #return uniValue
    def getSnapshotTimestamp(self, user, dbName):
        return self.getDb(user, dbName).getSnapshotTimestamp()

        
    def getSnapshotValueRange(self, user, dbName, key, timestamp, start, cnt):
        key = encodingTools.decodeToUnicode(key)
        res = self.getDb(user, dbName).getSnapshotValueRange(key, timestamp, start, cnt)
        #print res
        return res
        
        
    def appendValues(self, user, dbName, key, value):
        '''
        This value will be called in info collection from infoDb
        '''
        key = encodingTools.decodeToUnicode(key)
        #print 'appending:',value,type(value)
        if not (type(value) == list):
            value = [value]
        uniValue = []
        for i in value:
            uniValue.append(encodingTools.decodeToUnicode(i))
        self.getDb(user, dbName).append(key, uniValue)
        try:
            #Invliad the item
            del self.cache[(user, dbName,key)]
        except KeyError:
            pass

        #print 'appended----------------------------------------------------'
        #print 'append:', user, dbName, key, uniValue
        #return uniValue
    def bulkAdd(self, user, dbName, bulkDict):
        '''
        This function is used in jstreeOnCollectionV2
        '''
        #print 'entering bulk add'
        encDict = {}
        for i in bulkDict:
            value = bulkDict[i]
            if not (type(value) == list):
                value = [value]
            encValueList = []
            for j in value:
                print 'adding value:', i, j
                encValueList.append(encodingTools.decodeToUnicode(j))
            encDict[encodingTools.decodeToUnicode(i)] = encValueList
            try:
                #Invliad the item
                del self.cache[(user, dbName, encodingTools.decodeToUnicode(i))]
            except KeyError:
                pass
        self.getDb(user, dbName).bulkAdd(encDict)
        #print encDict
        #print 'bulk add done'
        #return encDict

        
        
    def getKeys(self, user, dbName, start, end, timeStamp):
        return self.getDb(user, dbName).keys()

server.register_instance(dictDbRpcServer())

# Run the server's main loop
server.serve_forever()