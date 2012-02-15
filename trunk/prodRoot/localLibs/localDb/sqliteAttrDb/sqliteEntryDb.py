import localLibSys
import wwjufsdatabase.libs.ufsDb.ufsDbBaseInterface as ufsDbBaseInterface
import sqlite3 as sqlite
import sys

def ncl(s):
    pass

class sqliteEntryDb(ufsDbBaseInterface.ufsSimpleDbEntryDbInterface):
    def __init__(self, entryDbOwer, dbFullPath):
        self.entryDbOwer = entryDbOwer
        self.sqlFsDb = sqlite.connect(dbFullPath)
        self.sqlFsCur = self.sqlFsDb.cursor()
        try:
            create_cmd = 'CREATE TABLE sqlfsdb (id INTEGER PRIMARY KEY\
            , uuid VARCHAR(512)\
            , keyid INTEGER\
            , valueid INTEGER\
            , create_date DATE\
            , createapp VARCHAR(512)\
            , owner VARCHAR(512))'
            #print create_cmd
            self.sqlFsCur.execute(create_cmd)
            self.sqlFsDb.commit()
        except:
            #The table does not exist, create table
            #print "exist"
            pass

    def getObjIdList(self, keyId, valueId, offset = 0, limit = 20):
        t = (keyId, valueId, limit, offset)
        query_cmd = 'SELECT uuid from sqlfsdb WHERE keyid = ? AND valueid = ? LIMIT ? OFFSET ?'
        ncl(query_cmd)
        result = sqlFsCur.execute(query_cmd, t)
       
        valueList = list()
        for e in result:
          valueid = e[0]
          #print valueid
          ncl(valueid)
          valueList.append(valueid)
        return valueList

    def add(self, objId, keyId, valueId, createapp):
        '''
        If the item already exists, then it will not be added again
        '''
        t = (objId, keyId, valueId, self.entryDbOwer)
        query_cmd = 'SELECT * FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND valueid = ? AND owner = ?'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        #quit if it exists.
        for e in result:
          return
        t = (objId, keyId, valueId, createapp, self.entryDbOwer)
        query_cmd = 'INSERT INTO sqlfsdb(uuid, keyid, valueid, create_date, createapp, owner) VALUES (?, ?, ?, DATETIME("NOW"), ?, ?)'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        self.sqlFsDb.commit()
    def update(self, objId, keyId, valueId, newValueId):
        self.delete(objId, keyId, valueId)
        self.add(objId, keyId, newValueId)
        self.commit()
    def hasKey(self, keyId):
        t = (objId, keyId, self.entryDbOwer)
        query_cmd = 'SELECT * FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND owner = ?'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        #quit if it exists.
        for e in result:
          return

    def delete(self, objId, keyId, valueId):
        t = (uuid, keyid, valueid)
        query_cmd = 'DELETE FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND valueid = ?'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        self.sqlFsDb.commit()
    def runInTransaction(self, f):
        pass
    def getAttrList(self, objId, key, offset = 0, limit = 20):
        t = (objId, keyId, self.entryDbOwer)
        query_cmd = 'SELECT * FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND owner = ?'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        #quit if it exists.
        for e in result:
          return
