#import libs.GAE.session
# import libs.http.queryParam
# import libs.platform.services
#from libs.platform.ufsDbManagerInterface import *

def showStorage():
    import libs.services.services
    s = libs.services.services.services()

    f = s.getQuery()
    #print f['sessionId']
    #print f['sessionId'][0]

    print "Content-Type: text/html;charset=utf-8"
    print ""
    print f

    user = s.getUserAutoRedirect('/apps/test/ufsStorageShow.py')
    if user is None:
        h.genEnd()
        return
    print '\'\'\'\'----------------'
    print 'OK'
    print s.uid

    import libs.platform.ufsDbManagerInterface

    u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
    m = libs.platform.ufsDbManagerInterface.ufsDbManager()
    db = m.getStorageDb(u, 'testStorageDb')
    print 'the real data is:<br/>'
    print db.getData('df2352b3-6dd9-4073-915f-e25ef829ac3e')