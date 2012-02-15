#Only import the dbSys class so it can be changed in the future by modify only this file.
import dbSysOnReq.dbSysSmart as dbSysSmart
#Usage:
'''
#Obsoleted method:
import libs.ufsDb.ufsDbSys as dbSys
dbSysInst = dbSys.dbSysSmart()

#Recommended method:
import libs.service.servicV2 as service
r = service.req()
r.getDbSys()
'''