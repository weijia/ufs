

def deleteItem():
    import libs.services.services
    s = libs.services.services.services()
    h = s.getHtmlGen()
    h.genTxtHead()
    import uuid
    dataId = str(uuid.uuid4())
    print '{"uuid":"%s"}'%dataId

    import libs.platform.services
    q = libs.platform.services.getQueryService()
    f = q.getAllFieldStorage()


    import libs.platform.ufsDbManagerInterface
    mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

    user = s.getUserAutoRedirect('/apps/tree/updateItem.py')
    if user is None:
        h.genEnd()
        return


    u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
    if f.has_key('treeImporterDb'):
      dbName = f['treeImporterDb'][0]
    else:
      dbName = 'treeImporterDb'
    db = mngr.getSimpleDb(u, dbName)
    nameDb = mngr.getSimpleDb(u, 'treeImporterNameDb')
    import libs.services.nameService
    nS = libs.services.nameService.nameService(nameDb)

    testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
    treeRoot = f.get('itemId', [testRoot])[0]

    if treeRoot == '0':
      treeRoot = testRoot

    import libs.tree.namedTreeItem
    i = libs.tree.namedTreeItem.namedTreeItem(treeRoot, db, nS)

    i.delete()


deleteItem()



