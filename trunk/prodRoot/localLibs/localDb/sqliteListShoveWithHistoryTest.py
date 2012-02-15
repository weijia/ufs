import sqliteListShoveWithHistory


s = sqliteListShoveWithHistory.Shove('d:/tmp/testCollection.sqlite')


import localLibSys
import wwjufsdatabase.libs.collection.collectionBase as collectionBase


c = collectionBase.collectionBase(u'collectionTestId',s)
c.append(u'good')
c.append(u'bad')
c.append(u'ok')
c.append(u'notok')
print c.hasElem(u'good')
print c.hasElem(u'nogood')
print c.getRange(1,2)
print c.getRange(0,10)
c.remove(u'ok')
print c.getRange(0,10)
c.refresh()
print c.getRange(0,10)
