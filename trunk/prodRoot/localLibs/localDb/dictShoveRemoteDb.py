import os
#------------------------------------------------------------------
#Remote database
import libs.cache.shoveClientV4 as listShoveClient 
def getRemoteDb(dbName):
    return listShoveClient.Shove(dbName)

import libs.cache.shoveClientV5 as shoveClient
def getSingleValueRemoteDb(dbName):
    return shoveClient.Shove(dbName)
