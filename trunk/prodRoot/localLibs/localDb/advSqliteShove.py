

import sqliteShoveV2

class advSqliteListShove(sqliteShoveV2.Shove):
    def append(self, key, valueOrList):
        if type(key) != unicode:
            raise nonUnicode
        if type(valueOrList) == unicode:
            valueOrList = [valueOrList]
        elif type(valueOrList) != list:
            raise nonSupportedValueType
        for i in valueOrList:
            if type(i) != unicode:
                raise nonUnicode
            t = (key, i)
            try:
                self.c.execute('insert into kv values(? , ?, datetime("now"))', t)
            except sqlite3.OperationalError:
                self.c.execute('insert into kv values(? , ?)', t)
            #print 'inserting ',t
        self.db.commit()
    def remove(self, key, valueOrList):
        if type(key) != unicode:
            raise nonUnicode
        if type(valueOrList) == unicode:
            valueOrList = [valueOrList]
        elif type(valueOrList) != list:
            raise nonSupportedValueType
        for i in valueOrList:
            if type(i) != unicode:
                raise nonUnicode
            t = (key, i)
            self.c.execute('delete from kv where key=? AND value = ?', t)
        self.db.commit()