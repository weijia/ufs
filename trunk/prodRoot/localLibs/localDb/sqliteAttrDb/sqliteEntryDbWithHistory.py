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
            , owner VARCHAR(512)\
            , removed INTEGER\
            , updated_date DATE)'
            #print create_cmd
            self.sqlFsCur.execute(create_cmd)
            self.sqlFsDb.commit()
        except:
            #The table does not exist, create table
            #print "exist"
            pass

    def getObjIdList(self, keyId, valueId, offset = 0, limit = 20):
        t = (keyId, valueId, limit, offset)
        query_cmd = 'SELECT uuid from sqlfsdb WHERE keyid = ? AND valueid = ? AND removed = 0 LIMIT ? OFFSET ?'
        ncl(query_cmd)
        result = self.sqlFsCur.execute(query_cmd, t)
       
        valueList = []
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
        query_cmd = 'SELECT * FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND valueid = ? AND owner = ? AND removed = 0'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        #quit if it exists.
        for e in result:
          return
        t = (objId, keyId, valueId, createapp, self.entryDbOwer)
        query_cmd = 'INSERT INTO sqlfsdb(uuid, keyid, valueid, create_date, createapp, owner, removed, updated_date) VALUES (?, ?, ?, DATETIME("NOW"), ?, ?, 0, DATETIME("NOW"))'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        self.sqlFsDb.commit()
    def update(self, objId, keyId, valueId, newValueId):
        self.delete(objId, keyId, valueId)
        self.add(objId, keyId, newValueId)
        self.commit()
    def hasKey(self, keyId):
        t = (objId, keyId, self.entryDbOwer)
        query_cmd = 'SELECT * FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND owner = ? AND removed = 0'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        #quit if it exists.
        for e in result:
          return

    def delete(self, objId, keyId, valueId):
        query_cmd = 'UPDATE sqlfsdb SET removed = 1, updated_data = DATETIME("NOW") WHERE uuid = "%s" AND keyid = %d AND valueid = %d'%(uuid, keyid, valueid)
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd)
        self.sqlFsDb.commit()
        
    def commit(self):
        self.sqlFsDb.commit()
        
    def runInTransaction(self, f):
        pass
    def getAttrList(self, objId, keyId, offset = 0, limit = 20):
        t = (objId, keyId, self.entryDbOwer, limit, offset)
        query_cmd = 'SELECT valueid FROM sqlfsdb WHERE uuid = ? AND keyid = ? AND owner = ? AND removed = 0 LIMIT ? OFFSET ?'
        #t = (offset, limit)
        #query_cmd = 'SELECT valueid FROM sqlfsdb LIMIT 20 OFFSET 0'
        #print query_cmd
        result = self.sqlFsCur.execute(query_cmd, t)
        res = []
        #quit if it exists.
        for e in result:
          res.append(e[0])
        return res