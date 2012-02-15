import urllib
import libSys
#import libs.platform.ufsDbManagerInterface.ufsUserExample
import libs.platform.ufsDbManagerInterface

#u = libs.platform.ufsDbManagerInterface.ufsUserExample('tester')
import libs.ufsDb.ufsClient

u = libs.ufsDb.ufsClient.ufsClient()
u.login('test1', 'testpass')
print u.sid

m = libs.platform.ufsDbManagerInterface.ufsDbManager()
d = m.getSimpleDbClient(u, 'testDb')
import uuid
d.add(str(uuid.uuid4()), 'testKey', 'testValue')