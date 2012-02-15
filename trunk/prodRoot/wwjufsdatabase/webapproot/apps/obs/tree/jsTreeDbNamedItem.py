#import libs.GAE.session
import libs.http.queryParam
import libs.platform.services
import libs.tree.jsTreeNamedItemFunc
import libs.platform.ufsDbManagerInterface
import libs.tree.namedTreeItem
import libs.services.nameService


def namedItem():
    import libs.services.services
    s = libs.services.services.services()

    print "Content-Type: text/html;charset=utf-8"
    print ""

    f = s.getQuery()

    mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()
    user = s.getUser()
    if user is None:
        #print 'user is None'
        user = 'tester'
    else:
        #print 'user is logged in'
        pass
    u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
    if f.has_key('treeImporterDb'):
      dbName = f['treeImporterDb'][0]
    else:
      dbName = 'treeImporterDb'
    db = mngr.getSimpleDb(u, dbName)
    nameDb = mngr.getSimpleDb(u, 'treeImporterNameDb')
    nS = libs.services.nameService.nameService(nameDb)
    bigValueDb = mngr.getSimpleDbWithBigValue(u, 'treeImporterBigValueDb')

    itemId = f.get('id',[libs.tree.dbTreeItem.sysGlobalTreeRoot])[0]
    treeRoot = f.get('treeRoot',[libs.tree.dbTreeItem.sysGlobalTreeRoot])[0]
    if itemId == '-1':
      print '''<li id = "%s" class="jstree-closed"><a href="#">/</a></li>
    '''%treeRoot
    else:
      #print '''<li id="%s" class="closed"><a href="#"><ins>&nbsp;</ins>%s</a></li><li><a href="#"><ins>&nbsp;</ins>Node 2</a></li>'''%(f, f['id'][0])
      d = itemId
      res = ''
      print '<!--'
      
      n = libs.tree.namedTreeItem.namedTreeItem(d, db, nS, bigValueDb)
      res = libs.tree.jsTreeNamedItemFunc.dirlist(n)
      print '-->'
      #print res,d
      print res
      
      
namedItem()