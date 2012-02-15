import dbus.service
import dbusServiceBase
#import localLibSys



################################################################
#Required !!! Override the following interface name
INTERFACE_NAME = 'com.wwjufsdatabase.logService'

class logService(dbusServiceBase.dbusServiceBase):

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def logStr(self, logStr):
        print logStr
        return "OK"

        
        
        
def getServiceObj(sessionBus, objectPath, configDictInst):
    return logService(sessionBus, objectPath, configDictInst)