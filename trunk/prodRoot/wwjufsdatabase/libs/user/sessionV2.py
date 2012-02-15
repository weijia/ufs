import localLibSys
from localLibs.logSys.logSys import *


class sessionInterface:
    def __init__(self, sessionId, shoveLikeInstance):
        pass
    def __getitem__(self, key):
        pass
    def __setitem__(self, key, value):
        pass
        
        
class session:
    def __init__(self, sessionId, shoveLikeInstance):
        self.db = shoveLikeInstance
        self.sessionId = sessionId
    def __getitem__(self, key):
        #ncl(self.sessionId+key)
        return self.db[self.sessionId+key]
    def __setitem__(self, key, value):
        self.db[self.sessionId+key] = value
        #ncl(self.sessionId+key+"="+value)
    def append(self, key, value):
        self.db.append(self.sessionId+key, value)