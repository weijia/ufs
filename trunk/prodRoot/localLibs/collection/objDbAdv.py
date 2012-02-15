'''
Created on Sep 27, 2011

@author: Richard
'''

import localLibSys
import localLibs.objSys.objectDatabaseV3 as objectDatabase
import wwjufsdatabase.libs.utils.objTools as objTools
from localLibs.logSys.logSys import *

class objectDatabase(objectDatabase.objectDatabase):
    '''
    This is an object db without any local filesystem operation
    '''
    def getSameObjList(self, fullPath):
        o = self.getFsObjFromFullPath(fullPath)
        if o is None:
            return []
        size = o["size"]
        items = self.objDb.find({"size": size})
        res = []
        for i in items:
            if i["uuid"] == o["uuid"]:
                continue
            if (i["headMd5"] == o["headMd5"]):
                ncl(i["headMd5"], o["headMd5"])
                res.append(i["fullPath"])
        return res
    
        
