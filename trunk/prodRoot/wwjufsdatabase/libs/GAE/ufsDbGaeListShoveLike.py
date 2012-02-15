from google.appengine.ext import db

gGaeShoveDbObjId = 'bc04ad1b-4ebc-4d5f-969c-fbf2f5e85433'
gMaxGaeSupportedItem = 900
class keysNotSupported: pass
import UserDict

class shoveLike(UserDict.DictMixin):
    def __init__(self, ufsBaseDbInstance):
        self.db = ufsBaseDbInstance
        
    def __getitem__(self, key):
        #return self.db.getAttrList(gGaeShoveDbObjId, key, 1, 1000)
        return self.getRange(key, 0, None)
    
    def __setitem__(self, key, value):
        self.db.add(gGaeShoveDbObjId, key, value)
    
    def __delitem__(self, gGaeShoveDbObjId, key):
        l = self.__getitem__(gGaeShoveDbObjId, key)
        for i in l:
            self.db.delete(gGaeShoveDbObjId, key, i)
    
    def keys(self):
        raise keysNotSupported()
        
    def getSnapshotTimestamp(self):
        return 0
    def getSnapshotValueRange(self, key, timeStamp, start, cnt):
        #return ['Test item']
        return self.getRange(key, start, cnt)
    def getRange(self, key, start, cnt):
        if cnt is None:
            res = []
            while True:
                tmpRes = self.db.getAttrList(gGaeShoveDbObjId, key, start, gMaxGaeSupportedItem)
                res.extend(tmpRes)
                start += gMaxGaeSupportedItem
                if len(tmpRes) < gMaxGaeSupportedItem:
                    break
            #res.append("test item")
            #res.append(key)
            #res.append(unicode(str(start)))
            return res
        res = self.db.getAttrList(gGaeShoveDbObjId, key, start, cnt)
        #res.append(key)
        #res.append(unicode(str(start)))
        #res.append(unicode(str(cnt)))
        #return ['Test item']
        return res
    def append(self, key, value):
        self.db.add(gGaeShoveDbObjId, key, value)