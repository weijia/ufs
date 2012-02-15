import shoveClientV4 as listShoveClient
import UserDict

class Shove(UserDict.DictMixin):
    def __init__(self, dbName):
        self.listDb = listShoveClient.Shove(dbName)
    def __getitem__(self, key):
        v = self.listDb[key]
        return v[0]
    def __setitem__(self, key, value):
        self.listDb[key] = value

    def __delitem__(self, key):
        del self.listDb[key]

