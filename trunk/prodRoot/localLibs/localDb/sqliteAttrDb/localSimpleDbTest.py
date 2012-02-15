import sqliteEntryDbWithHistory as sqliteEntryDb
import sqliteTokenDb
import localLibSys
import wwjufsdatabase.libs.ufsDb.ufsDbBase as ufsDbBase

def main():
    tokenDb = sqliteTokenDb.sqliteTokenDb('d:/tmp/tokenDbTest.sqlite')
    entryDb = sqliteEntryDb.sqliteEntryDb('testOwner', 'd:/tmp/entryDbTest.sqlite')
    db = ufsDbBase.ufsSimpleDbBase(tokenDb, entryDb)
    db.add('first', 'good','bad')
    db.add('second', 'good','bad')
    db.add('first','ok','nack')
    db.add('first','ok','notnack')
    db.add('second','ok','notnack')
    print db.getAttrList('first', 'ok')
    print db.getObjIdList('good','bad')
    
    

if __name__ == '__main__':
    main()
